// Copyright (C) 2022-2025 Intel Corporation
// LIMITED EDGE SOFTWARE DISTRIBUTION LICENSE

interface ParameterBase {
    key: string;
    name: string;
    description: string;
}

export interface NumberParameter extends ParameterBase {
    type: 'int' | 'float';
    value: number;
    minValue: number;
    maxValue: number | null;
    defaultValue: number;
}

export interface ArrayParameter extends ParameterBase {
    type: 'array';
    value: number[];
    defaultValue: number[];
}

export interface BoolParameter extends ParameterBase {
    type: 'bool';
    value: boolean;
    defaultValue: boolean;
}

interface EnumParameter<T extends boolean | number> extends ParameterBase {
    type: 'enum';
    value: T;
    defaultValue: T;
    allowedValues: T[];
}

export interface StaticParameter extends ParameterBase {
    value: number | boolean;
}

export type EnumConfigurationParameter = EnumParameter<number>;

export type ConfigurationParameter = BoolParameter | NumberParameter | EnumConfigurationParameter | ArrayParameter;

interface ProjectConfigurationTaskConfigsTraining {
    constraints: ConfigurationParameter[];
}

interface ProjectConfigurationTaskConfigs {
    taskId: string;
    training: ProjectConfigurationTaskConfigsTraining;
    autoTraining: ConfigurationParameter[];
}

export type KeyValueParameter = Pick<ConfigurationParameter, 'key' | 'value'>;

export interface ProjectConfigurationUploadPayload {
    taskConfigs: {
        taskId: string;
        training?: {
            constraints: KeyValueParameter[];
        };
        autoTraining?: KeyValueParameter[];
    }[];
}

export interface ProjectConfiguration {
    taskConfigs: ProjectConfigurationTaskConfigs[];
}

export type DatasetPreparationParameters = {
    subsetSplit: ConfigurationParameter[];
    filtering: Record<string, ConfigurationParameter[]>;
    augmentation: Record<string, ConfigurationParameter[]>;
};

export type TrainingParameters = (ConfigurationParameter | Record<string, ConfigurationParameter[]>)[];

export interface TrainingConfiguration {
    datasetPreparation: DatasetPreparationParameters;
    training: TrainingParameters;
    evaluation: ConfigurationParameter[];
    taskId: string;
}

export interface TrainedModelConfiguration extends Omit<TrainingConfiguration, 'datasetPreparation'> {
    datasetPreparation: Pick<DatasetPreparationParameters, 'augmentation'>;
    advancedConfiguration: StaticParameter[];
}

export type TrainingConfigurationUpdatePayload = TrainingConfiguration;
