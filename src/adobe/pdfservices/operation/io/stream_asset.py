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

class StreamAsset:
    """
    This class encapsulates input stream and the media type of
    :class:`Asset<adobe.pdfservices.operation.io.asset.Asset>`.
    """
    def __init__(self, input_stream, mime_type):
        """
        Constructs an instance of :samp:`StreamAsset`.

        :param input_stream: input stream of the asset; can not be None.
        :param mime_type: mime type of the input stream; can not be None.
        :type mime_type: str
        """
        self.input_stream = input_stream
        self.mime_type = mime_type

    def get_input_stream(self):
        """
        :return: the input stream of the asset.
        """
        return self.input_stream

    def get_mime_type(self):
        """
        :return: the mime type of the asset.
        :rtype: str
        """
        return self.mime_type
