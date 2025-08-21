// Copyright (C) 2022-2025 Intel Corporation
// LIMITED EDGE SOFTWARE DISTRIBUTION LICENSE

import { ReactElement, ReactNode } from 'react';

import { Flex, Heading, Text, View } from '@adobe/react-spectrum';
import { clsx } from 'clsx';
import { isEmpty } from 'lodash-es';
import { toast as soonerToast, Toaster, ToastT } from 'sonner';

import { AcceptCircle, Alert, CloseSmall, CrossCircle, Info } from '../../icons';
import { ActionButton } from '../button/button.component';
import { Divider } from '../divider/divider.component';

import classes from './toast.module.scss';

type ToastType = 'success' | 'error' | 'warning' | 'info' | 'neutral';

type ToastProps = {
    id?: string;
    type: ToastType;
    actionButtons?: ReactElement[];
    hasCloseButton?: boolean;
    duration?: number;
    onDismiss?: () => void;
    message: ReactNode;
    position?: ToastT['position'];
    title?: string;
};

type CustomToastProps = {
    id: string;
    type: ToastType;
    message: ReactNode;
    actionButtons?: ReactElement[];
    hasCloseButton?: boolean;
    title?: string;
};

const ICON: Record<ToastType, ReactNode> = {
    success: <AcceptCircle />,
    error: <CrossCircle />,
    warning: <Alert />,
    info: <Info />,
    neutral: null,
};

const ToastCloseButton = ({ id }: { id: string }) => {
    return (
        <ActionButton
            isQuiet
            onPress={() => soonerToast.dismiss(id)}
            aria-label={'Close toast'}
            UNSAFE_className={classes.closeButton}
        >
            <CloseSmall className={classes.closeIcon} />
        </ActionButton>
    );
};

const ToastContainer = ({ children, type }: { children: ReactNode; type: ToastType }) => {
    const toastTypeStyles = classes[type];

    return (
        <div aria-label={'toast'} className={clsx(toastTypeStyles, classes.toast)}>
            {children}
        </div>
    );
};

const ToastActionButtons = ({ actionButtons }: { actionButtons?: ReactElement[] }) => {
    if (isEmpty(actionButtons)) {
        return null;
    }

    return (
        <Flex alignItems={'center'} UNSAFE_className={classes.actionButtons}>
            {actionButtons}
        </Flex>
    );
};

const CustomToast = ({ message, id, actionButtons, type, hasCloseButton = true, title }: CustomToastProps) => {
    const icon = ICON[type];

    if (title === undefined) {
        return (
            <ToastContainer type={type}>
                <Flex
                    width={'100%'}
                    height={'100%'}
                    justifyContent={'space-between'}
                    alignItems={'center'}
                    gap={'size-200'}
                >
                    <Flex flex={1} alignItems={'center'} justifyContent={'space-between'}>
                        <Flex gap={'size-100'} alignItems={'center'}>
                            <View>{icon}</View>
                            <Text>{message}</Text>
                        </Flex>
                        <ToastActionButtons actionButtons={actionButtons} />
                    </Flex>

                    {hasCloseButton && (
                        <Flex height={'100%'} alignItems={'center'} gap={'size-50'}>
                            <Divider
                                orientation={'vertical'}
                                height={'size-400'}
                                size={'M'}
                                UNSAFE_className={classes.toastDivider}
                            />
                            <ToastCloseButton id={id} />
                        </Flex>
                    )}
                </Flex>
            </ToastContainer>
        );
    }

    return (
        <ToastContainer type={type}>
            <Flex width={'100%'} justifyContent={'space-between'}>
                <Flex direction={'column'} gap={'size-100'}>
                    <Flex alignItems={'baseline'} gap={'size-100'}>
                        <View>{icon}</View>
                        <Heading level={2} margin={0}>
                            {title}
                        </Heading>
                    </Flex>
                    <Text>{message}</Text>
                    <ToastActionButtons actionButtons={actionButtons} />
                </Flex>
                <ToastCloseButton id={id} />
            </Flex>
        </ToastContainer>
    );
};

const DEFAULT_TOAST_DURATION = 8000;

export const removeToast = (id: string | number) => {
    if (isEmpty(id)) return;

    soonerToast.dismiss(id);
};

export const removeToasts = () => {
    const toasts = soonerToast.getToasts();
    toasts.forEach((toast) => {
        removeToast(toast.id);
    });
};

const parseId = (text: string) => {
    return text.split(' ').join('-').replace(',', '').toLowerCase();
};

export const toast = ({
    id,
    message,
    actionButtons,
    hasCloseButton,
    type,
    duration = DEFAULT_TOAST_DURATION,
    onDismiss,
    position,
    title,
}: ToastProps) => {
    const toastId = `id-${parseId(id ?? String(message))}`;

    return soonerToast.custom(
        () => {
            return (
                <CustomToast
                    id={toastId}
                    type={type}
                    message={message}
                    actionButtons={actionButtons}
                    hasCloseButton={hasCloseButton}
                    title={title}
                />
            );
        },
        {
            id: toastId,
            // We don't want error notifications to dismiss automatically.
            // For all the others, we dismiss them after {duration}
            duration: type === 'error' ? Infinity : duration,
            onDismiss,
            position,
            className: classes.toastContainer,
        }
    );
};

export const Toast = () => {
    return <Toaster position='bottom-center' className={classes.toaster} />;
};
