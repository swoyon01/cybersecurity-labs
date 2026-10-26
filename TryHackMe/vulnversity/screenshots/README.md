# Screenshots / evidence

This folder holds evidence from the Vulnversity lab. The included file is the screenshot supplied in the conversation; it shows the service link/enable steps and `/bin/bash` with permissions `-rwsr-xr-x`.


<img width="1280" height="684" alt="Screenshot 2026-10-27 005242" src="https://github.com/user-attachments/assets/9212eb9d-01dc-46f3-a9a6-46678043542c" />

<img width="1280" height="684" alt="Screenshot 2026-10-27 010000" src="https://github.com/user-attachments/assets/47e79e2d-3d4b-404a-b4c1-3f7dc14148ea" />
<img width="1280" height="684" alt="Screenshot 2026-10-27 010715" src="https://github.com/user-attachments/assets/73a7d3aa-4adf-4626-92b5-9fe4b9308274" />
<img width="1280" height="684" alt="Screenshot 2026-10-27 005900" src="https://github.com/user-attachments/assets/4e5f62eb-83d6-47ce-b02c-3308c3c57493" />

<img width="1280" height="684" alt="Screenshot 2026-10-27 010813" src="https://github.com/user-attachments/assets/98da4f50-3de6-458c-856c-db73289fd66b" />
<img width="1280" height="684" alt="Screenshot 2026-10-27 011003" src="https://github.com/user-attachments/assets/088943e7-985c-4220-93b1-c25593443f2b" />
<img width="1280" height="684" alt="Screenshot 2026-10-27 011104" src="https://github.com/user-attachments/assets/f30c8cf1-fdfd-41f4-a04c-bb05bb26ad05" />
<img width="1280" height="684" alt="Screenshot 2026-10-27 013852" src="https://github.com/user-attachments/assets/2491f2df-d034-4fac-9de3-cada9ffd08cd" />

<img width="1280" height="684" alt="Screenshot 2026-10-27 014232" src="https://github.com/user-attachments/assets/f4c1daa9-b0a2-4280-ae83-2f165f561707" />
<img width="1280" height="684" alt="Screenshot 2026-10-27 014745" src="https://github.com/user-attachments/assets/97afdf35-9e83-4e07-b895-769ee361bcc2" />
<img width="1280" height="684" alt="Screenshot 2026-10-27 015055" src="https://github.com/user-attachments/assets/2916e096-f297-48bd-8933-62bce4449ba4" />
<img width="1280" height="684" alt="Screenshot 2026-10-27 020029" src="https://github.com/user-attachments/assets/00cf2cbd-f416-4d01-8e49-86244be572dd" />
<img width="1280" height="684" alt="Screenshot 2026-10-27 020512" src="https://github.com/user-attachments/assets/f030fda3-e4e5-45da-9720-3a5f1a605e85" />


The included screenshot also shows an earlier `Permission denied` when `/root/root.txt` was checked before escalation. The lower portion proves the Bash SUID bit was later set; capture a new screenshot after verifying `euid=0(root)` for final root proof.

