// Copyright (C) 2022-2025 Intel Corporation
// LIMITED EDGE SOFTWARE DISTRIBUTION LICENSE

import {
    NumberParameter,
    TrainingConfiguration,
} from '../../../../../../../../core/configurable-parameters/services/configuration.interface';
import { isNumberParameter } from '../../../../../../../../core/configurable-parameters/utils';

type SubsetSplitParameters = TrainingConfiguration['datasetPreparation']['subsetSplit'];

const getDatasetSize = (subsetSplitParameters: SubsetSplitParameters): number => {
    const datasetSize = subsetSplitParameters.find((parameter) => parameter.key === 'dataset_size');

    if (isNumberParameter(datasetSize)) {
        return datasetSize.value;
    }

    return 0;
};

export const getSubsetsSizes = (
    subsetSplitParameters: SubsetSplitParameters,
    validationSubsetRatio: number,
    testSubsetRatio: number
) => {
    const datasetSize = getDatasetSize(subsetSplitParameters);

    const validationSubsetSize = Math.floor(datasetSize * (validationSubsetRatio / 100));
    const testSubsetSize = Math.floor(datasetSize * (testSubsetRatio / 100));
    const trainingSubsetSize = datasetSize - validationSubsetSize - testSubsetSize;

    return {
        trainingSubsetSize,
        validationSubsetSize,
        testSubsetSize,
    };
};

export const MAX_RATIO_VALUE = 100;

export const TEST_SUBSET_KEY = 'test';
export const VALIDATION_SUBSET_KEY = 'validation';
export const TRAINING_SUBSET_KEY = 'training';

export const getSubsets = (subsetsParameters: TrainingConfiguration['datasetPreparation']['subsetSplit']) => {
    const validationSubset = subsetsParameters.find(
        (parameter) => parameter.key === VALIDATION_SUBSET_KEY
    ) as NumberParameter;
    const trainingSubset = subsetsParameters.find(
        (parameter) => parameter.key === TRAINING_SUBSET_KEY
    ) as NumberParameter;
    const testSubset = subsetsParameters.find((parameter) => parameter.key === TEST_SUBSET_KEY) as NumberParameter;

    return {
        trainingSubset,
        validationSubset,
        testSubset,
    };
};

export const areSubsetsSizesValid = (subsetParameters: SubsetSplitParameters): boolean => {
    const { validationSubset, testSubset } = getSubsets(subsetParameters);

    const newSubsetSizes = getSubsetsSizes(subsetParameters, validationSubset.value, testSubset.value);

    return ![
        newSubsetSizes.trainingSubsetSize,
        newSubsetSizes.validationSubsetSize,
        newSubsetSizes.testSubsetSize,
    ].some((size) => size === 0);
};
