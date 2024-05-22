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

from typing import List

from adobe.pdfservices.operation.internal.api.dto.request.pagemanipulation.page_actions import PageActions
from adobe.pdfservices.operation.internal.execution_context import ExecutionContext
from adobe.pdfservices.operation.internal.params.combine_pdf_job_input import CombinePDFJobInput
from adobe.pdfservices.operation.internal.util.object_util import ObjectUtil
from adobe.pdfservices.operation.internal.util.string_util import StringUtil
from adobe.pdfservices.operation.io.asset import Asset
from adobe.pdfservices.operation.pdfjobs.params.documentmerge.document_merge_params import DocumentMergeParams
from adobe.pdfservices.operation.pdfjobs.params.eseal.csc_credentials import CSCCredentials
from adobe.pdfservices.operation.pdfjobs.params.eseal.electronic_seal_params import PDFElectronicSealParams
from adobe.pdfservices.operation.pdfjobs.params.eseal.field_location import FieldLocation
from adobe.pdfservices.operation.pdfjobs.params.eseal.field_options import FieldOptions
from adobe.pdfservices.operation.pdfjobs.params.page_ranges import PageRanges
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.encryption_algorithm import EncryptionAlgorithm
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.password_protect_params import PasswordProtectParams
from adobe.pdfservices.operation.pdfjobs.params.protect_pdf.protect_pdf_params import ProtectPDFParams


class ValidationUtil:
    __SPLIT_PDF_OUTPUT_COUNT_LIMIT = 20
    __REMOVE_PROTECTION_PASSWORD_MAX_LENGTH = 150
    __PASSWORD_MAX_LENGTH = 128
    __PAGE_ACTIONS_MAX_LIMIT = 200

    @classmethod
    def validate_execution_context(cls, context: ExecutionContext):
        ObjectUtil.require_not_null(context, "Context not initialized before invoking the operation")

    @classmethod
    def validate_asset_with_page_options(cls, combine_pdf_job_input: CombinePDFJobInput):
        ObjectUtil.require_not_null(combine_pdf_job_input.get_asset(), "No input asset was set for the submitted job")
        cls.validate_page_options(combine_pdf_job_input)

    @classmethod
    def validate_page_options(cls, combine_pdf_job_input: CombinePDFJobInput):
        page_ranges: PageRanges = combine_pdf_job_input.get_page_ranges()
        if page_ranges is None:
            raise ValueError("No page options provided for combining files PDFs")
        page_ranges.validate()

    @classmethod
    def validate_pdf_electronic_seal_params(cls, pdf_electronic_seal_params: PDFElectronicSealParams):
        if pdf_electronic_seal_params is None:
            raise ValueError("PDF Electronic Seal Params cannot be None")

        if pdf_electronic_seal_params.get_seal_certificate_credentials() is None:
            raise ValueError("Certificate credentials cannot be None")

        if pdf_electronic_seal_params.get_seal_field_options() is None:
            raise ValueError("Field options cannot be None")

        csc_credential: CSCCredentials = pdf_electronic_seal_params.get_seal_certificate_credentials()
        cls.validate_csc_credential(csc_credential)

        field_options = pdf_electronic_seal_params.get_seal_field_options()
        cls.validate_field_options(field_options)

    @classmethod
    def validate_csc_credential(cls, csc_credential: CSCCredentials):
        if StringUtil.is_blank(csc_credential.get_credential_id()):
            raise ValueError("Credential ID in CSC credentials cannot be None or empty")
        if StringUtil.is_blank(csc_credential.get_pin()):
            raise ValueError("Pin in CSC credentials cannot be None or empty")
        if csc_credential.get_csc_auth_context() is None:
            raise ValueError("Auth context in CSC credentials cannot be None")
        if StringUtil.is_blank(csc_credential.get_csc_auth_context().get_access_token()):
            raise ValueError("Access token in auth context for CSC credentials cannot be None or empty")
        if StringUtil.is_blank(csc_credential.get_provider_name()):
            raise ValueError("Provider name in CSC credentials cannot be None or empty")
        if StringUtil.is_blank(csc_credential.get_csc_auth_context().get_token_type()):
            raise ValueError("Token type in auth context for CSC credentials cannot be None or empty")

    @classmethod
    def validate_field_options(cls, field_options: FieldOptions):
        if StringUtil.is_blank(field_options.get_field_name()):
            raise ValueError("Field name in field options cannot be None or empty")

        if field_options.get_page_number() is not None and field_options.get_page_number() <= 0:
            raise ValueError("Page number in field options is invalid.")

        field_location = field_options.get_field_location()
        if field_location is not None:
            cls.validate_field_location(field_location)

    @classmethod
    def validate_field_location(cls, field_location: FieldLocation):
        if field_location.get_left() is None:
            raise ValueError("Left coordinate in field location cannot be None")
        if field_location.get_top() is None:
            raise ValueError("Top coordinate in field location cannot be None")
        if field_location.get_right() is None:
            raise ValueError("Right coordinate in field location cannot be None")
        if field_location.get_bottom() is None:
            raise ValueError("Bottom coordinate in field location cannot be None")

    @classmethod
    def validate_protect_pdf_params(cls, protect_pdf_params: ProtectPDFParams):
        # Validations for PasswordProtectOptions
        if isinstance(protect_pdf_params, PasswordProtectParams):
            password_protect_params: PasswordProtectParams = protect_pdf_params

            # Validate encryption algorithm
            if password_protect_params.get_encryption_algorithm() is None:
                raise ValueError("Encryption algorithm cannot be None")

            if (StringUtil.is_blank(password_protect_params.get_owner_password()) and
                    StringUtil.is_blank(password_protect_params.get_user_password())):
                raise ValueError("One of the passwords (user/owner) is required")

            if (not StringUtil.is_blank(password_protect_params.get_owner_password()) and
                    not StringUtil.is_blank(password_protect_params.get_user_password()) and
                    password_protect_params.get_owner_password() == password_protect_params.get_user_password()):
                raise ValueError("User and owner password cannot be the same")

            # Validate user password
            if not StringUtil.is_blank(password_protect_params.get_user_password()):
                cls.validate_password(password_protect_params.get_user_password(), True,
                                      password_protect_params.get_encryption_algorithm())

            # Validate owner password
            if not StringUtil.is_blank(password_protect_params.get_owner_password()):
                cls.validate_password(password_protect_params.get_owner_password(), False,
                                      password_protect_params.get_encryption_algorithm())

            # OwnerPassword is mandatory in case the permissions are provided
            if (password_protect_params.get_permissions() is not None and
                    StringUtil.is_blank(password_protect_params.get_owner_password())):
                raise ValueError("The document permissions cannot be applied without setting the owner password")

    @classmethod
    def validate_password(cls, password: str, is_user_password: bool, encryption_algorithm: EncryptionAlgorithm):
        if len(password) == 0:
            raise ValueError(f"{('User' if is_user_password else 'Owner')} Password cannot be empty")

        if len(password) > cls.__PASSWORD_MAX_LENGTH:
            raise ValueError(
                f"{('User' if is_user_password else 'Owner')} Password length cannot exceed {cls.__PASSWORD_MAX_LENGTH} bytes")

        # Password validation for AES_128 encryption algorithm
        if encryption_algorithm == EncryptionAlgorithm.AES_128:
            try:
                password.encode('iso-8859-1')
            except UnicodeEncodeError:
                raise ValueError(
                    f"{('User' if is_user_password else 'Owner')} Password supports only LATIN-1 characters for AES-128 encryption")

    @classmethod
    def validate_insert_asset_inputs(cls, base_asset: Asset, assets_to_insert: {int, List[CombinePDFJobInput]}):
        if base_asset is None:
            raise ValueError("Base asset cannot be None")

        if assets_to_insert is None or len(assets_to_insert) == 0:
            raise ValueError("No assets to insert in the base input asset")

        for page_number, combine_pdf_job_inputs in assets_to_insert.items():
            if page_number < 1:
                raise ValueError("Base file page should be greater than 0")

            for combine_pdf_job_input in combine_pdf_job_inputs:
                cls.validate_page_ranges(combine_pdf_job_input.get_page_ranges())

    @classmethod
    def validate_replace_files_inputs(cls, base_asset: Asset, assets_to_replace: {int, CombinePDFJobInput}):
        if base_asset is None:
            raise ValueError("Base asset cannot be None")

        if assets_to_replace is None or len(assets_to_replace) == 0:
            raise ValueError("No assets to replace in the base input asset")

        for page_number, combine_pdf_job_input in assets_to_replace.items():
            if page_number < 1:
                raise ValueError("Base asset page should be greater than 0")

            cls.validate_page_ranges(combine_pdf_job_input.get_page_ranges())

    @classmethod
    def validate_page_ranges(cls, page_ranges: PageRanges):
        if page_ranges is None or page_ranges.is_empty():
            raise ValueError("No page ranges were set for the operation")

        page_ranges.validate()

    @classmethod
    def validate_rotate_page_actions(cls, page_actions: PageActions):
        if page_actions.is_empty():
            raise ValueError("No rotation specified for the operation")

        if page_actions.get_length() > cls.__PAGE_ACTIONS_MAX_LIMIT:
            raise ValueError("Too many rotations not allowed.")

        for page_action in page_actions.get_actions():
            if not page_action.get_page_ranges():
                raise ValueError("No page ranges were set for the operation")
            cls.validate_page_ranges(page_action.get_page_ranges())

    @classmethod
    def validate_password_to_remove_protection(cls, password: str):
        if StringUtil.is_blank(password):
            raise ValueError("Password cannot be empty")

        if len(password) > cls.__REMOVE_PROTECTION_PASSWORD_MAX_LENGTH:
            raise ValueError(
                f"Allowed maximum length of password is {cls.__REMOVE_PROTECTION_PASSWORD_MAX_LENGTH} characters")

    @classmethod
    def validate_split_pdf_operation_params(cls, page_ranges: PageRanges, page_count: int, file_count: int):
        if page_ranges is None and page_count is None and file_count is None:
            raise ValueError(
                "One of the options (page ranges/file count/page count) is required for splitting a PDF document")

        if page_ranges is not None:
            if page_count is not None or file_count is not None:
                raise ValueError(
                    "Only one of option (page ranges/page count/file count) can be specified for splitting a PDF document")

            if len(page_ranges.get_ranges()) > cls.__SPLIT_PDF_OUTPUT_COUNT_LIMIT:
                raise ValueError("Too many page ranges specified")

            cls.validate_page_ranges_overlap(page_ranges)
            cls.validate_page_ranges(page_ranges)
            return

        if page_count is not None:
            if file_count is not None:
                raise ValueError(
                    "Only one of option (page ranges/page count/file count) can be specified for splitting a PDF document")

            if page_count <= 0:
                raise ValueError("Page count should be greater than 0")
            return

        if file_count <= 0:
            raise ValueError("File count should be greater than 0")

        if file_count > cls.__SPLIT_PDF_OUTPUT_COUNT_LIMIT:
            raise ValueError(
                f"Input PDF file cannot be split into more than {cls.__SPLIT_PDF_OUTPUT_COUNT_LIMIT} documents")

    @classmethod
    def validate_page_ranges_overlap(cls, page_ranges: PageRanges):

        # Creating a copy in case the pageRange order matters in the original pageRanges
        page_range_list = sorted(page_ranges.get_ranges(), key=lambda x: x.get_start())

        for i in range(1, len(page_range_list)):
            if page_range_list[i - 1].get_end() is None or page_range_list[i].get_start() <= page_range_list[
                i - 1].get_end():
                raise ValueError("Overlapping page ranges are not allowed")

    @classmethod
    def validate_document_merge_params(cls, document_merge_params: DocumentMergeParams):
        if document_merge_params.get_json_data_for_merge() is None:
            raise ValueError("Input JSON data cannot be None")

        if not document_merge_params.get_json_data_for_merge():
            raise ValueError("Input JSON data cannot be empty")

        if document_merge_params.get_output_format() is None:
            raise ValueError("Output format cannot be None")
