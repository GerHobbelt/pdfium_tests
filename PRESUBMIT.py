# Copyright 2017 The PDFium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Presubmit script for PDFium testing corpus.

See http://dev.chromium.org/developers/how-tos/depottools/presubmit-scripts
for more details about the presubmit API built into depot_tools.
"""

def _CheckPngNames(input_api, output_api):
  """Checks that .png files have the right file name pattern"""
  import re
  png_regex = re.compile('.+_expected(_(win|mac|linux))?\.pdf\.\d+.png')
  warnings = []
  for f in input_api.AffectedFiles(include_deletes=False):
    local_path = f.LocalPath()
    if local_path.endswith('.png'):
      if not png_regex.match(local_path):
        warnings.append(local_path)

  results = []
  if warnings:
    results.append(output_api.PresubmitPromptOrNotify(
        'The following PNG files have the wrong file name format:\n',
        warnings))
  return results


def CheckChangeOnUpload(input_api, output_api):
  results = []
  results += _CheckPngNames(input_api, output_api)
  return results
