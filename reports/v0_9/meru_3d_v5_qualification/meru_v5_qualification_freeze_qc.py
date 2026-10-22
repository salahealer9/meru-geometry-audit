#!/usr/bin/env python3
"""Read-only V5 archive identity & manifest checker. No scientific imports, no projection."""
import hashlib,json,zipfile,sys
from pathlib import Path
p=Path(__file__).resolve().parent
exp={
 'MERU_3D_V5_READ_ONLY_QUALIFICATION_REVIEW_2026-10-22.zip': ('42fa29c800d58a4df7f8230e48db4e4271b9521fb0d6e9fa1adfb603dedbc7f7',5),
 'MERU_3D_V5_SECOND_INDEPENDENT_READ_ONLY_REVIEW_2026-10-22.zip': ('567e2017f4b6ef2717800ecd44ebedde100c6f5e84027180eee744c42f1ac13c',15),
 'MERU_3D_V5_R2_A1_FOCUSED_REQUALIFICATION_2026-10-22.zip': ('5f698ee6a74d45322efbb61382dd6ef3c7e74bbd5383dab515fcf32422b893ab',11),
 'MERU_3D_V5_R2_A1_THIRD_REVIEW_STAGE2_FINAL_2026-10-22.zip': ('cabe304cc27a6105643aa3d86b82827395e254167deff0b8709282fcc3b34be0',16),
}
sha=lambda b:hashlib.sha256(b).hexdigest()
results={}
for name,(target,count) in exp.items():
 raw=(p/name).read_bytes(); assert sha(raw)==target,name
 with zipfile.ZipFile(p/name) as z:
  assert z.testzip() is None,name
  mf=next(n for n in z.namelist() if n.endswith('/SHA256SUMS.txt'))
  pref=mf.rsplit('/',1)[0]+'/'
  lines=[line for line in z.read(mf).decode().splitlines() if line.strip()]
  assert len(lines)==count,(name,len(lines),count)
  for line in lines:
   h,f=line.split(maxsplit=1)
   assert sha(z.read(pref+f.strip()))==h,(name,f)
 results[name]={'sha256':target,'verified_internal_manifest_entries':count,'status':'PASS'}
with zipfile.ZipFile(p/'MERU_3D_V5_R2_A1_THIRD_REVIEW_STAGE2_FINAL_2026-10-22.zip') as z:
 pref='V5_R2_A1_third_review/'
 for fn,expected in [
 ('THIRD_REVIEW_BLIND_PROOF.md','0f398922a863b051c667c450576d5ba7c303e1eeb1530538cac90f991e16a1b9'),
 ('STAGE1_SEAL_RECEIPT.md','3656f682dfb0936601d14606d5dfa4c7ae40129acf82e69f2abcd2d92794791e')]:
  assert sha((p/fn).read_bytes())==expected
  assert z.read(pref+fn)==(p/fn).read_bytes(),fn
 qc=json.loads(z.read(pref+'THIRD_REVIEW_FINAL_QC.json'))
 assert 'QUALIFIED' in json.dumps(qc), 'third status mismatch'
 results['blind_proof_and_receipt']={'status':'PASS','proof_sha256':'0f398922a863b051c667c450576d5ba7c303e1eeb1530538cac90f991e16a1b9','seal_sha256':'3656f682dfb0936601d14606d5dfa4c7ae40129acf82e69f2abcd2d92794791e'}
assert all(x['status']=='PASS' for x in results.values())
print(json.dumps({'result':'PASS_ARCHIVE_IDENTITY_AND_MANIFEST_ONLY','checks':results,'scope':'no scientific experiment, no Git GPG verification'},indent=2,sort_keys=True))
