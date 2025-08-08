# Copyright (C) 2022-2025 Intel Corporation
# LIMITED EDGE SOFTWARE DISTRIBUTION LICENSE
from enum import Enum, auto


class DefaultCategory(str, Enum):
    """Model optimization preference categories.

    Defines the trade-off preference between accuracy and inference speed:
    - DEFAULT: The recommended model choice when no specific optimization preference is specified
    - ACCURACY: Models optimized for highest prediction quality, potentially at the cost of speed
    - SPEED: Models optimized for fastest inference time, potentially at the cost of accuracy
    - BALANCE: Models that provide a balanced trade-off between accuracy and speed
    """

    DEFAULT = auto()
    ACCURACY = auto()
    SPEED = auto()
    BALANCE = auto()


class TaskType(str, Enum):
    CLASSIFICATION = auto()
    DETECTION = auto()
    ROTATED_DETECTION = auto()
    INSTANCE_SEGMENTATION = auto()
    SEGMENTATION = auto()
    ANOMALY = auto()
    KEYPOINT_DETECTION = auto()


class DefaultModels:
    """Provides the recommended model architectures for different computer vision tasks.

    This class maps task types to recommended model architectures based on optimization
    preferences (accuracy, speed, or balance), offering a curated selection of pre-configured
    models suitable for various computer vision applications.
    """

    default_models_by_task: dict[TaskType, dict[DefaultCategory, str | None]] = {
        TaskType.CLASSIFICATION: {
            DefaultCategory.DEFAULT: "Custom_Image_Classification_EfficinetNet-B0",
            DefaultCategory.ACCURACY: "Custom_Image_Classification_EfficientNet-V2-S",
            DefaultCategory.SPEED: "Custom_Image_Classification_MobileNet-V3-large-1x",
            DefaultCategory.BALANCE: "Custom_Image_Classification_EfficinetNet-B0",
        },
        TaskType.DETECTION: {
            DefaultCategory.DEFAULT: "Custom_Object_Detection_Gen3_ATSS",
            DefaultCategory.ACCURACY: "Object_Detection_DFine_X",
            DefaultCategory.SPEED: "Object_Detection_YOLOX_S",
            DefaultCategory.BALANCE: "Custom_Object_Detection_Gen3_ATSS",
        },
        TaskType.ROTATED_DETECTION: {
            DefaultCategory.DEFAULT: "Rotated_Detection_MaskRCNN_ResNet50_V2",
            DefaultCategory.ACCURACY: "Rotated_Detection_MaskRCNN_ResNet50_V2",
            DefaultCategory.SPEED: "Custom_Rotated_Detection_via_Instance_Segmentation_MaskRCNN_EfficientNetB2B",
            DefaultCategory.BALANCE: None,
        },
        TaskType.INSTANCE_SEGMENTATION: {
            DefaultCategory.DEFAULT: "Custom_Counting_Instance_Segmentation_MaskRCNN_EfficientNetB2B",
            DefaultCategory.ACCURACY: "Custom_Counting_Instance_Segmentation_MaskRCNN_SwinT_FP16",
            DefaultCategory.SPEED: "Custom_Counting_Instance_Segmentation_MaskRCNN_EfficientNetB2B",
            DefaultCategory.BALANCE: "Custom_Instance_Segmentation_MaskRCNN_ResNet50_v2",
        },
        TaskType.SEGMENTATION: {
            DefaultCategory.DEFAULT: "Custom_Semantic_Segmentation_Lite-HRNet-18-mod2_OCR",
            DefaultCategory.ACCURACY: "Custom_Semantic_Segmentation_DINOV2_S",
            DefaultCategory.SPEED: "Custom_Semantic_Segmentation_Lite-HRNet-s-mod2_OCR",
            DefaultCategory.BALANCE: "Custom_Semantic_Segmentation_Lite-HRNet-18-mod2_OCR",
        },
        TaskType.ANOMALY: {
            DefaultCategory.DEFAULT: "ote_anomaly_padim",
            DefaultCategory.ACCURACY: "ote_anomaly_uflow",
            DefaultCategory.SPEED: "ote_anomaly_padim",
            DefaultCategory.BALANCE: None,
        },
        TaskType.KEYPOINT_DETECTION: {
            DefaultCategory.DEFAULT: "Keypoint_Detection_RTMPose_Tiny",
            DefaultCategory.ACCURACY: None,
            DefaultCategory.SPEED: "Keypoint_Detection_RTMPose_Tiny",
            DefaultCategory.BALANCE: None,
        },
    }

    @classmethod
    def get_model_by_type(cls, task_type: str, default_type: DefaultCategory) -> str | None:
        """
        Retrieve a recommended model architecture for a specific task and optimization preference.

        :param task_type: The computer vision task category
        :param default_type: The optimization preference (accuracy, speed, or balance)
        :return: The name of the recommended model architecture, or None if no model is available
        :raises ValueError: If the task_type or default_type is not supported
        """
        try:
            task_type_str = task_type.upper()
            if task_type_str == "VISUAL_PROMPTING":
                return None
            _task_type = TaskType[task_type_str]
        except KeyError:
            raise ValueError(f"Unknown task type: `{task_type}`")
        if default_type not in cls.default_models_by_task[_task_type]:
            raise ValueError(f"Unknown default type: {default_type} for task: {task_type}")
        return cls.default_models_by_task[_task_type][default_type]

    @classmethod
    def get_default_model(cls, task_type: str) -> str | None:
        """
        Gets the default model architecture for a specific computer vision task.

        :param task_type: The computer vision task category
        :return: The name of the default model architecture, or None if not available
        :raises ValueError: If the task_type is not supported
        """
        return cls.get_model_by_type(task_type, DefaultCategory.DEFAULT)

    @classmethod
    def get_accuracy_model(cls, task_type: str) -> str | None:
        """
        Gets the model architecture that prioritizes prediction quality over inference speed.

        :param task_type: The computer vision task category
        :return: The name of the accuracy-optimized model architecture, or None if not available
        :raises ValueError: If the task_type is not supported
        """
        return cls.get_model_by_type(task_type, DefaultCategory.ACCURACY)

    @classmethod
    def get_speed_model(cls, task_type: str) -> str | None:
        """
        Gets the model architecture that prioritizes inference speed over prediction quality.

        :param task_type: The computer vision task category
        :return: The name of the speed-optimized model architecture, or None if not available
        :raises ValueError: If the task_type is not supported
        """
        return cls.get_model_by_type(task_type, DefaultCategory.SPEED)

    @classmethod
    def get_balanced_model(cls, task_type: str) -> str | None:
        """
        Gets the model architecture that offers a compromise between accuracy and speed.

        :param task_type: The computer vision task category
        :return: The name of the balanced model architecture, or None if not available
        :raises ValueError: If the task_type is not supported
        """
        return cls.get_model_by_type(task_type, DefaultCategory.BALANCE)

    @classmethod
    def get_default_models_per_task(cls) -> dict[str, str | None]:
        """
        Gets the default model for each task type.

        :return: A dictionary mapping task types to their default model names
        """
        return {task_type.name.lower(): cls.get_default_model(task_type.name.lower()) for task_type in TaskType}
