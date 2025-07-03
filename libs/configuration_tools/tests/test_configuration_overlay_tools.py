# Copyright (C) 2022-2025 Intel Corporation
# LIMITED EDGE SOFTWARE DISTRIBUTION LICENSE
import pytest
from geti_types import ID

from geti_configuration_tools import ConfigurationOverlayTools
from geti_configuration_tools.hyperparameters import (
    AugmentationParameters,
    CenterCrop,
    DatasetPreparationParameters,
    EarlyStopping,
    EvaluationParameters,
    Hyperparameters,
    TrainingHyperParameters,
)
from geti_configuration_tools.training_configuration import (
    Filtering,
    GlobalDatasetPreparationParameters,
    GlobalParameters,
    MaxAnnotationObjects,
    MaxAnnotationPixels,
    MinAnnotationObjects,
    MinAnnotationPixels,
    PartialTrainingConfiguration,
    SubsetSplit,
    TrainingConfiguration,
)


@pytest.fixture
def ftx_hyperparameters():
    yield Hyperparameters(
        dataset_preparation=DatasetPreparationParameters(
            augmentation=AugmentationParameters(
                center_crop=CenterCrop(enable=True, ratio=0.6),
            )
        ),
        training=TrainingHyperParameters(
            max_epochs=100,
            early_stopping=EarlyStopping(enable=True, patience=10),
            learning_rate=0.001,
        ),
        evaluation=EvaluationParameters(),
    )


@pytest.fixture
def fxt_global_parameters():
    yield GlobalParameters(
        dataset_preparation=GlobalDatasetPreparationParameters(
            subset_split=SubsetSplit(
                training=70,
                validation=20,
                test=10,
                auto_selection=True,
                remixing=False,
            ),
            filtering=Filtering(
                min_annotation_pixels=MinAnnotationPixels(enable=True, min_annotation_pixels=10),
                max_annotation_pixels=MaxAnnotationPixels(enable=True, max_annotation_pixels=1000),
                min_annotation_objects=MinAnnotationObjects(enable=True, min_annotation_objects=5),
                max_annotation_objects=MaxAnnotationObjects(enable=True, max_annotation_objects=100),
            ),
        )
    )


@pytest.fixture
def fxt_training_configuration_task_level(fxt_global_parameters, ftx_hyperparameters):
    yield TrainingConfiguration(
        id_=ID("training_config_id"),
        task_id="task_123",
        global_parameters=fxt_global_parameters,
        hyperparameters=ftx_hyperparameters,
    )


class TestConfigurationService:
    @pytest.mark.parametrize(
        "d, expected",
        [
            # Empty dict
            ({}, {}),
            # Dict with no None values
            ({"a": 1, "b": "test"}, {"a": 1, "b": "test"}),
            # Dict with None values
            ({"a": 1, "b": None, "c": "test"}, {"a": 1, "c": "test"}),
            # Dict with nested dict containing None values
            ({"a": 1, "b": {"x": None, "y": 2}}, {"a": 1, "b": {"y": 2}}),
            # Dict with list containing dicts with None values
            ({"a": 1, "b": [{"x": None, "y": 2}, {"z": 3}]}, {"a": 1, "b": [{"y": 2}, {"z": 3}]}),
            # Complex nested scenario
            (
                {"a": 1, "b": None, "c": {"d": None, "e": {"f": None, "g": 2}, "h": [{"i": None, "j": 3}]}},
                {"a": 1, "c": {"e": {"g": 2}, "h": [{"j": 3}]}},
            ),
        ],
    )
    def test_delete_none_from_dict(self, d, expected) -> None:
        result = ConfigurationOverlayTools.delete_none_from_dict(d)
        assert result == expected
        # Ensure the function modifies the dict in-place
        assert result is d

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            # Empty dicts
            ({}, {}, {}),
            # Empty target dict
            ({}, {"x": 1}, {"x": 1}),
            # Empty source dict
            ({"x": 1}, {}, {"x": 1}),
            # Non-overlapping keys
            ({"x": 1}, {"y": 2}, {"x": 1, "y": 2}),
            # Overlapping keys (non-dict values)
            ({"x": 1}, {"x": 2}, {"x": 2}),
            # Simple nested dict
            ({"x": 1, "y": {"a": 2}}, {"y": {"b": 3}, "z": 4}, {"x": 1, "y": {"a": 2, "b": 3}, "z": 4}),
            # Complex nested scenario
            (
                {"a": 1, "b": {"c": 2, "d": {"e": 3}}},
                {"b": {"d": {"f": 4}, "g": 5}},
                {"a": 1, "b": {"c": 2, "d": {"e": 3, "f": 4}, "g": 5}},
            ),
            # Overwrite dict with non-dict
            ({"a": {"b": 1}}, {"a": 2}, {"a": 2}),
            # Overwrite non-dict with dict
            ({"a": 1}, {"a": {"b": 2}}, {"a": {"b": 2}}),
        ],
    )
    def test_merge_deep_dict(self, a, b, expected) -> None:
        result = ConfigurationOverlayTools.merge_deep_dict(a, b)
        assert result == expected
        # Ensure the function modifies the first dict in-place
        assert result is a

    def test_overlay_configurations(self, fxt_training_configuration_task_level) -> None:
        # Arrange
        # Create base configuration
        base_partial_config = PartialTrainingConfiguration(
            task_id="task_123",
            global_parameters={
                "dataset_preparation": {
                    "subset_split": {"training": 70, "validation": 20, "test": 10, "auto_selection": True},
                    "filtering": {"min_annotation_pixels": {"enable": False, "min_annotation_pixels": 1}},
                }
            },
        )

        # Create overlay configuration with some changes
        overlay_config_1 = PartialTrainingConfiguration(
            task_id="task_123",
            global_parameters={
                "dataset_preparation": {
                    "subset_split": {"training": 60, "validation": 30, "test": 10, "remixing": True},
                    "filtering": {"max_annotation_pixels": {"enable": True, "max_annotation_pixels": 5000}},
                }
            },
            hyperparameters={
                "training": {
                    "max_epochs": 32,
                    "learning_rate": 0.01,
                }
            },
        )

        overlay_config_2 = PartialTrainingConfiguration(
            task_id="task_123", hyperparameters={"training": {"learning_rate": 0.05}}
        )

        expected_partial_overlay_config = PartialTrainingConfiguration(
            task_id="task_123",
            global_parameters={
                "dataset_preparation": {
                    "subset_split": {
                        "training": 60,
                        "validation": 30,
                        "test": 10,
                        "remixing": True,
                        "auto_selection": True,
                    },
                    "filtering": {
                        "min_annotation_pixels": {"enable": False, "min_annotation_pixels": 1},
                        "max_annotation_pixels": {"enable": True, "max_annotation_pixels": 5000},
                    },
                }
            },
            hyperparameters={
                "training": {
                    "max_epochs": 32,
                    "learning_rate": 0.05,  # This should be the last value applied
                }
            },
        )

        # Act
        full_config_overlay = ConfigurationOverlayTools.overlay_training_configurations(
            fxt_training_configuration_task_level, base_partial_config, overlay_config_1, overlay_config_2
        )
        partial_overlay = ConfigurationOverlayTools.overlay_training_configurations(
            base_partial_config, overlay_config_1, overlay_config_2, validate_full_config=False
        )

        # Assert
        full_config_dataset_preparation = full_config_overlay.global_parameters.dataset_preparation
        assert partial_overlay.model_dump() == expected_partial_overlay_config.model_dump()
        assert full_config_dataset_preparation.subset_split.training == 60
        assert full_config_dataset_preparation.subset_split.validation == 30
        assert full_config_dataset_preparation.subset_split.remixing
        assert full_config_dataset_preparation.filtering.max_annotation_pixels.enable
        assert not full_config_dataset_preparation.filtering.min_annotation_pixels.enable
        assert full_config_dataset_preparation.filtering.min_annotation_pixels.min_annotation_pixels == 1
        assert full_config_overlay.hyperparameters.training.max_epochs == 32
        assert full_config_overlay.hyperparameters.training.learning_rate == 0.05
