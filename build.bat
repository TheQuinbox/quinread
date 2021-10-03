@echo off
nuitka --windows-company-name=Accessware --windows-product-name=Quinread --windows-file-version=1.0 --windows-product-version=1.0 --windows-file-description=Quinread --standalone --python-flag=no_site --windows-disable-console --remove-output quinread.pyw
pause > nul
