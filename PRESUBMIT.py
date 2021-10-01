# Copyright 2017 The PDFium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Presubmit script for PDFium testing corpus.

See http://dev.chromium.org/developers/how-tos/depottools/presubmit-scripts
for more details about the presubmit API built into depot_tools.
"""

def _CheckNoIn(input_api, output_api):
  """Checks that corpus tests don't contain .in files. Corpus tests should be
  .pdf files, having both can cause race conditions on the bots, which run the
  tests in parallel.
  """
  results = []
  for f in input_api.AffectedFiles(include_deletes=False):
    if f.LocalPath().endswith('.in'):
      results.append(output_api.PresubmitError(
          'Remove %s since corpus tests should not use .in files' % f.LocalPath()))
  return results

def _CheckPngNames(input_api, output_api):
  """Checks that .png files have the right file name format, which must be in
  the form of
  NAME_expected(_(skia|skiapaths))?(_(win|mac|linux))?.pdf.#.png. This format
  must be the same as the one used in PDFium's PRESUBMIT.py's
  _CheckPNGFormat().
  """
  png_regex = input_api.re.compile(
      r'.+_expected(_(skia|skiapaths))?(_(win|mac|linux))?\.pdf\.\d+.png')
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
  results += _CheckNoIn(input_api, output_api)
  return results
