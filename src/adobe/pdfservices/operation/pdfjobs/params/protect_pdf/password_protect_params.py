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

from typing import Optional

from adobe.pdfservices.operation.internal.util.enforce_types import enforce_types
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.content_encryption import ContentEncryption
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.encryption_algorithm import EncryptionAlgorithm
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.permissions import Permissions
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.protect_pdf_params import ProtectPDFParams


class PasswordProtectParams(ProtectPDFParams):
    """
    Parameters for securing PDF file with passwords and document permissions using
    :class:`ProtectPDFJob<adobe.pdfservices.operation.pdfjobs.jobs.protect_pdf_job.ProtectPDFJob>`
    """

    @enforce_types
    def __init__(self, encryption_algorithm: EncryptionAlgorithm, *,
                 content_encryption: ContentEncryption = ContentEncryption.ALL_CONTENT,
                 permissions: Optional[Permissions] = None,
                 user_password: Optional[str] = None,
                 owner_password: Optional[str] = None):
        """
        Constructs a new :samp:`PasswordProtectParams` instance.

        :param encryption_algorithm: Sets the intended encryption algorithm required for encrypting the PDF file. For
            AES-128 encryption, the password supports LATIN-I characters only. For AES-256 encryption, passwords supports
            Unicode character set.
        :type encryption_algorithm: EncryptionAlgorithm
        :param content_encryption: Type of content to encrypt in the PDF file. (Optional, use key-value)
        :type content_encryption: ContentEncryption
        :param permissions: Sets the intended permissions for the encrypted PDF file. This includes permissions to allow
            printing, editing and content copying in the PDF document. Permissions can only be used in case the owner
            password is set. (Optional, use key-value)
        :type permissions: Permissions
        :param user_password: User password required for opening the encrypted PDF file. Allowed maximum length
            for the user password is 128 bytes. (Optional, use key-value)
        :type user_password: str
        :param owner_password: Owner password required to control access permissions in the encrypted PDF file. This
            password can also be used to open/view the encrypted PDF file. Allowed maximum length for the owner
            password is 128 bytes. (Optional, use key-value)
        :type owner_password: str
        """
        self.__user_password = user_password
        self.__owner_password = owner_password
        self.__encryption_algorithm = encryption_algorithm
        self.__content_encryption = content_encryption
        self.__permissions = permissions
        from adobe.pdfservices.operation.internal.util.validation_util import ValidationUtil
        ValidationUtil.validate_protect_pdf_params(self)

    def get_user_password(self):
        """
        :return: the intended user password of the resulting encrypted PDF file.
        :rtype: str
        """
        return self.__user_password

    def get_owner_password(self):
        """
        :return: the intended owner password of the resulting encrypted PDF file.
        :rtype: str
        """
        return self.__owner_password

    def get_encryption_algorithm(self):
        """
        :return: EncryptionAlgorithm of the resulting encrypted PDF file.
        :rtype: EncryptionAlgorithm
        """
        return self.__encryption_algorithm

    def get_content_encryption(self):
        """
        :return: ContentEncryption for the resulting encrypted PDF file as a string.
        :rtype: ContentEncryption
        """
        return self.__content_encryption

    def get_permissions(self):
        """
        :return: Permissions for the resulting encrypted PDF file.
        :rtype: Permissions
        """
        return self.__permissions
