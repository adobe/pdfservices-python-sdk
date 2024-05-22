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
from adobe.pdfservices.operation.pdfjobs.params.eseal.appearance_options import AppearanceOptions
from adobe.pdfservices.operation.pdfjobs.params.eseal.csc_credentials import CSCCredentials
from adobe.pdfservices.operation.pdfjobs.params.eseal.document_level_permission import DocumentLevelPermission
from adobe.pdfservices.operation.pdfjobs.params.eseal.field_options import FieldOptions
from adobe.pdfservices.operation.pdfjobs.params.eseal.signature_format import SignatureFormat
from adobe.pdfservices.operation.pdfjobs.params.eseal.tsa_options import TSAOptions


class PDFElectronicSealParams:
    """
    Parameters for electronically seal PDFs using
    :class:`PDFElectronicSealJob<adobe.pdfservices.operation.pdfjobs.jobs.eseal_job.PDFElectronicSealJob>`.
    """

    @enforce_types
    def __init__(self,
                 seal_certificate_credentials: CSCCredentials,
                 seal_field_options: FieldOptions, *,
                 seal_signature_format: SignatureFormat = SignatureFormat.PKCS7,
                 document_level_permissions: DocumentLevelPermission = DocumentLevelPermission.FORM_FILLING,
                 seal_appearance_options: Optional[AppearanceOptions] = None,
                 tsa_options: Optional[TSAOptions] = None
                 ):
        """
        Constructs a new :samp:`PDFElectronicSealParams` instance.

        :param seal_certificate_credentials: CertificateCredentials to be used for applying electronic seal; can not be None.
        :type seal_certificate_credentials: CSCCredentials
        :param seal_field_options: FieldOptions to be used for applying electronic seal; can not be None.
        :type seal_field_options: FieldOptions
        :param seal_signature_format: SignatureFormat to be used for applying electronic seal. (Optional, use key-value)
        :type seal_signature_format: SignatureFormat
        :param document_level_permissions: Document level permission for changes allowed after sealing. (Optional, use key-value)
        :type document_level_permissions: DocumentLevelPermission
        :param seal_appearance_options: AppearanceOptions for the seal. (Optional, use key-value)
        :type seal_appearance_options: AppearanceOptions
        :param tsa_options: Time stamp authority options. (Optional, use key-value)
        :type tsa_options: TSAOptions
        :return: A new instance of PDFElectronicSealParams
        :rtype: PDFElectronicSealParams
        """
        self._seal_certificate_credentials = seal_certificate_credentials
        self._seal_field_options = seal_field_options
        self._seal_signature_format = seal_signature_format
        self._seal_appearance_options = seal_appearance_options
        self._document_level_permissions = document_level_permissions
        self._tsa_options = tsa_options

    def to_dict(self):
        """
        For SDK's internal use

        :return: ElectronicSealParams as a dictionary.
        :rtype: dict
        """
        seal_options = {
            'signatureFormat': self._seal_signature_format.get_signature_format(),
            'documentLevelPermission': self._document_level_permissions.__str__(),
            'cscCredentialOptions': self._seal_certificate_credentials.to_dict(),
            'sealFieldOptions': self._seal_field_options.to_dict()
        }
        if self._seal_appearance_options is not None:
            seal_options['sealAppearanceOptions'] = {
                'displayOptions': self._seal_appearance_options.get_appearance_options()
            }
        if self._tsa_options is not None:
            seal_options['tsaOptions'] = self._tsa_options.to_dict()
        return seal_options

    def get_signature_format(self):
        """
        :return: SignatureFormat to be used for applying electronic seal.
        :rtype: SignatureFormat
        """
        return self._seal_signature_format

    def get_seal_certificate_credentials(self):
        """
        :return: CertificateCredentials to be used for applying electronic seal
        :rtype: CSCCredentials
        """
        return self._seal_certificate_credentials

    def get_seal_field_options(self):
        """
        :return: FieldOptions to be used for applying electronic seal.
        :rtype: FieldOptions
        """
        return self._seal_field_options

    def get_seal_appearance_options(self):
        """
        :return: AppearanceOptions for the seal.
        :rtype: AppearanceOptions
        """
        return self._seal_appearance_options
