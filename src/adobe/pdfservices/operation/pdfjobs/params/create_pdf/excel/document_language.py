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


class DocumentLanguage(Enum):
    """
    Supported locales for Excel to PDF.
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
    Represents "English (United States)" locale
    """

    ZH_HK = "zh-HK"
    """
    Represents "Chinese (Hong Kong)" locale
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
    Represents "Japanese (Japan)" locale.
    
    Please note that this locale is only supported for US(default) region.
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

    NO_NO = "no-NO"
    """
    Represents "Norwegian (Norway)" locale
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


    def __init__(self, document_language):
        self.document_language = document_language

    def get_document_language(self):
        return self.document_language
