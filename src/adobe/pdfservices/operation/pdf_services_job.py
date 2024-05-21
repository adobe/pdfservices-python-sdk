# Copyright 2024 Adobe
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Adobe and its suppliers, if any. The intellectual
# and technical concepts contained herein are proprietary to Adobe
# and its suppliers and are protected by all applicable intellectual
# property laws, including trade secret and copyright laws.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Adobe.

from abc import ABC, abstractmethod

from adobe.pdfservices.operation.config.notifier.notifier_config import NotifierConfig
from adobe.pdfservices.operation.internal.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.util.validation_util import ValidationUtil


class PDFServicesJob(ABC):
    """
    This abstract class represents the basic contract for all the PDF Services Jobs.
    It imposes no restrictions or particular details on the job execution process and leaves the
    specifics of setting up the jobs to their individual implementations.
    """

    def _validate(self, execution_context: ExecutionContext):
        ValidationUtil.validate_execution_context(execution_context)

    @abstractmethod
    def _process(self, execution_context: ExecutionContext, notifier_config: NotifierConfig = None) -> str:
        pass
