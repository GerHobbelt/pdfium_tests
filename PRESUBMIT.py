# Copyright 2017 The PDFium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Presubmit script for PDFium testing corpus.

See http://dev.chromium.org/developers/how-tos/depottools/presubmit-scripts
for more details about the presubmit API built into depot_tools.
"""

PRESUBMIT_VERSION = '2.0.0'

USE_PYTHON3 = True

def _CheckNoIn(input_api, output_api):
  """Checks that corpus tests don't contain .in files. Corpus tests should be
  .pdf files, having both can cause race conditions on the bots, which run the
  tests in parallel.
  """
  results = []
  for f in input_api.AffectedFiles(include_deletes=False):
    if f.LocalPath().endswith('.in'):
      results.append(output_api.PresubmitError(
          f'Remove {f.LocalPath()} since corpus tests should not use .in files'
      ))
  return results

def _CheckPngNames(input_api, output_api):
  """Checks that .png files have the right file name format, which must be in
  the form:

  NAME_expected(_(agg|skia))?(_(linux|mac|win))?.pdf.\d+.png

  This must be the same format as the one in PDFium's PRESUBMIT.py.
  """
  expected_pattern = input_api.re.compile(
      r'.+_expected(_(agg|skia))?(_(linux|mac|win))?\.pdf\.\d+.png')
  results = []
  for f in input_api.AffectedFiles(include_deletes=False):
    if not f.LocalPath().endswith('.png'):
      continue
    if expected_pattern.match(f.LocalPath()):
      continue
    results.append(
        output_api.PresubmitError(
            'PNG file %s does not have the correct format' % f.LocalPath()))
  return results

def ChecksCommon(input_api, output_api):
  results = []

  results.extend(
      input_api.canned_checks.PanProjectChecks(
          input_api, output_api, project_name='PDFium'))

  return results

def CheckChangeOnUpload(input_api, output_api):
  results = []
  results += _CheckPngNames(input_api, output_api)
  results += _CheckNoIn(input_api, output_api)
  return results
