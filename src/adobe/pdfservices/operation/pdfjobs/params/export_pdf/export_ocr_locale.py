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

from enum import Enum


class ExportOCRLocale(Enum):
    """
    Enum values representing different locales
    """

    DA_DK = "da-DK"
    """
    Represents "Danish (Denmark)" locale
    """

    LT_LT = "lt-LT"
    """
    Represents "Lithuanian (Lithuania)" locale
    """

    SL_SI = "sl-SI"
    """
    Represents "Slovenian (Slovenia)" locale
    """

    EL_GR = "el-GR"
    """
    Represents "Greek (Greece)" locale
    """

    RU_RU = "ru-RU"
    """
    Represents "Russian (Russia)" locale
    """

    EN_US = "en-US"
    """
    Represents "English (United States)" locale.
    """

    HU_HU = "hu-HU"
    """
    Represents "Hungarian (Hungary)" locale
    """

    ET_EE = "et-EE"
    """
    Represents "Estonian (Estonia)" locale
    """

    PT_BR = "pt-BR"
    """
    Represents "Portuguese (Brazil)" locale
    """

    UK_UA = "uk-UA"
    """
    Represents "Ukrainian (Ukraine)" locale
    """

    NB_NO = "nb-NO"
    """
    Represents "Norwegian (Norway)" locale
    """

    PL_PL = "pl-PL"
    """
    Represents "Polish (Poland)" locale
    """

    LV_LV = "lv-LV"
    """
    Represents "Latvian (Latvia)" locale
    """

    FI_FI = "fi-FI"
    """
    Represents "Finnish (Finland)" locale
    """

    JA_JP = "ja-JP"
    """
    Represents "Japanese (Japan)" locale
    """

    ES_ES = "es-ES"
    """
    Represents "Spanish (Spain)" locale
    """

    BG_BG = "bg-BG"
    """
    Represents "Bulgarian (Bulgaria)" locale
    """

    EN_GB = "en-GB"
    """
    Represents "English (United Kingdom)" locale
    """

    CS_CZ = "cs-CZ"
    """
    Represents "Czech (Czech Republic)" locale
    """

    MT_MT = "mt-MT"
    """
    Represents "Maltese (Malta)" locale
    """

    DE_DE = "de-DE"
    """
    Represents "German (Germany)" locale
    """

    HR_HR = "hr-HR"
    """
    Represents "Croatian (Croatia)" locale
    """

    SK_SK = "sk-SK"
    """
    Represents "Slovak (Slovakia)" locale
    """

    SR_SR = "sr-SR"
    """
    Represents "Serbian (Serbia)" locale
    """

    CA_CA = "ca-CA"
    """
    Represents "Catalan (Canada)" locale
    """

    MK_MK = "mk-MK"
    """
    Represents "Macedonian (Macedonia)" locale
    """

    KO_KR = "ko-KR"
    """
    Represents "Korean (Korea)" locale
    """

    DE_CH = "de-CH"
    """
    Represents "German (Switzerland)" locale
    """

    NL_NL = "nl-NL"
    """
    Represents "Dutch (Netherlands)" locale
    """

    ZH_CN = "zh-CN"
    """
    Represents "Chinese (China)" locale
    """

    SV_SE = "sv-SE"
    """
    Represents "Swedish (Sweden)" locale
    """

    IT_IT = "it-IT"
    """
    Represents "Italian (Italy)" locale
    """

    TR_TR = "tr-TR"
    """
    Represents "Turkish (Turkey)" locale
    """

    FR_FR = "fr-FR"
    """
    Represents "French (France)" locale
    """

    RO_RO = "ro-RO"
    """
    Represents "Romanian (Romania)" locale
    """

    IW_IL = "iw-IL"
    """
    Represents "Hebrew (Israel)" locale
    """

    PT_PT = "pt-PT"
    """
    Represents "European Portuguese" locale
    """

    NN_NO = "nn-NO"
    """
    Represents "Norwegian Nynorsk (Norway)" locale
    """

    ZH_HANT = "zh-Hant"
    """
    Represents "Chinese (traditional)" locale
    """

    EU_ES = "eu-ES"
    """
    Represents "Basque (Spain)" locale
    """

    GL_ES = "gl-ES"
    """
    Represents "Galician (Spain)" locale
    """

    def __init__(self, locale):
        """
        Constructs a locale from a language code

        :param locale: language code
        """
        self.locale = locale

    def get_export_ocr_locale(self):
        """
        :return: Language code of the ExportOCRLocale
        """
        return self.locale
