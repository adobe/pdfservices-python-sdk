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
from adobe.pdfservices.operation.pdfjobs.params.eseal.field_location import FieldLocation


class FieldOptions:
    """
    Parameters specifying options related to the seal field required for
    :class:`PDFElectronicSealParams<adobe.pdfservices.operation.pdfjobs.params.eseal.electronic_seal_params.PDFElectronicSealParams>`.
    """

    @enforce_types
    def __init__(self, field_name: str, *,
                 field_location: Optional[FieldLocation] = None,
                 page_number: Optional[int] = None,
                 visible: Optional[bool] = True):
        """
        Constructs a new instance of :samp:`FieldOptions`.

        :param field_name: The name of the field to be used for applying the electronic seal. If signature field with
            this field name already exist, that field will be used. If it does not exist, a signature field with this
            field name will be created. Can not be None.
        :type field_name: str
        :param field_location: A FieldLocation instance specifying coordinates for the electronic seal. The location
            is only required for visible signatures if the signature field does not already exist in the PDF document.
            If location is provided along with the existing signature field then it is ignored. (Optional, use key-value)
        :type field_location: FieldLocation
        :param page_number: The page number to which the signature field should be attached. Page numbers are 1-based.
            The page number is only required for visible signatures if the signature field does not already exist in
            the PDF document. If page number is provided along with the existing signature field then the page number
            should be same on which signature field is present in the document, else an error is thrown.
            (Optional, use key-value)
        :type page_number: int
        :param visible: The intended visibility flag for the electronic seal. Default value is true.
            (Optional, use key-value)
        :type visible: bool
        """
        self._field_name = field_name
        self._field_location = field_location
        self._page_number = page_number
        self._visible = visible

    def to_dict(self):
        field_options_dict = {
            'fieldName': self._field_name,
            'visible': self._visible
        }
        if self._field_location is not None:
            field_options_dict['location'] = self._field_location.to_dict()
        if self._page_number is not None:
            field_options_dict['pageNumber'] = self._page_number
        return field_options_dict

    def get_field_name(self):
        """
        :return: Field Name
        :rtype: str
        """
        return self._field_name

    def get_field_location(self):
        """
        :return: Field Location
        :rtype: FieldLocation
        """
        return self._field_location

    def get_page_number(self):
        """
        :return: Page Number
        :rtype: int
        """
        return self._page_number

    def get_visible(self):
        """
        :return: Visibility flag for the electronic seal
        :rtype: bool
        """
        return self._visible
