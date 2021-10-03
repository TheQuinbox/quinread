@echo off
nuitka --windows-company-name=Accessware --windows-product-name=Quinread --windows-file-version=0.1 --windows-product-version=0.1 --windows-file-description=Quinread --standalone --python-flag=no_site --windows-disable-console --remove-output quinread.pyw
pause > nul
