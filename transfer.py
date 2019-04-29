#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 09:38:14 2019

@author: mikaelapisanileal
"""

import dropbox
import os

#Transfer data to dropbox
class TransferData:
    def __init__(self, access_token, timeout):
        self.access_token = access_token
        self.CHUNK_SIZE = 4 * 1024 * 1024
        self.timeout = timeout

    def upload_file(self, file_from, file_to):
        dbx = dropbox.Dropbox(self.access_token, timeout=self.timeout)
        f = open(file_from, 'rb')
        file_size = os.path.getsize(file_from)
        upload_session_start_result = dbx.files_upload_session_start(f.read(self.CHUNK_SIZE))
        cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                           offset=f.tell())
        commit = dropbox.files.CommitInfo(path=file_to)
        
        while f.tell() < file_size:
            if ((file_size - f.tell()) <= self.CHUNK_SIZE):
                dbx.files_upload_session_finish(f.read(self.CHUNK_SIZE),
                                                cursor,
                                                commit)
            else:
                dbx.files_upload_session_append(f.read(self.CHUNK_SIZE),
                                                cursor.session_id,
                                                cursor.offset)
                cursor.offset = f.tell()


