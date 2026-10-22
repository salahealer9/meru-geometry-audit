# QO2D-M1 operator evidence-copy scope

The original `evidence/run_01` folder on the user’s Linux machine was created by the previously supplied run-once command. Its files are copied in without modification. They are not reconstructed by the signing package and this package does not execute Python or other experiments.

Expected original run members (verify they are present):

- results.json
- stderr.txt (operator reported empty; must be verified zero bytes)
- exit_code.txt
- script_sha256.txt
- output_sha256.txt
- preregistration_commit.txt
- python_version.txt
- start_utc.txt
- end_utc.txt

The Python script is copied from `~/meru-qo2d-m1/qo2d_m1_standalone_calculator.py`. Independent review was created by ChatGPT and is not an independent organizational audit. Files supplied to ChatGPT for comparison were `results.json` and `exit_code.txt`; the remaining operator metadata remain preserved as source records rather than separately witnessed records.

`EVIDENCE_SHA256SUMS.txt` is rooted at the Git repository's top level. It records the four available source/review hashes and the empty stderr hash. Its successful verification attests local byte matches to those known identities, not execution chronology or software correctness.
