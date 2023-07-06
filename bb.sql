SELECT 

	 A.F0132_CROSS_KEY'account'
	,A.R_TR_TR_AC_CODE'code'
	,A.R_TR_DESC'desc'
	,A.R_TR_TOTAL_AMT'amount'
	,B.F0262_PROCEEDS_AMOUNT'proceeds'
	,B.F0148_LATE_CHARGES_DUE_AMOUNT'late'
	,B.F0571_MISC_FEES_DUE_AMOUNT'fees'
	,A.R_TR_PRIN'prin pmt'
	,CONVERT(DATE, A.R_TR_EFF_DTE)'EFF DATE'
	--,ISNULL(C.F0264_DEALER_HOLDBACK, 0)

FROM

	[SHAW_HISTORY].[dbo].[DWR_RETAIL_TRAN_HISTORY] A
	LEFT JOIN SHAW_EOD.DBO.DWR_RETAIL B ON  B.F0132_CROSS_KEY = A.F0132_CROSS_KEY
	LEFT JOIN SHAW_EOD.DBO.DWR_RETAIL C ON C.F0132_CROSS_KEY = A.F0132_CROSS_KEY

WHERE 

	SUBSTRING(A.F0132_CROSS_KEY, 1, 11) IN ('17273190002',
'17329150002',
'17372670003')
	--AND R_TR_DESC NOT IN ('NULL')
	--AND A.F0000_PROCESS_DATE BETWEEN '01/01/2023' AND '05/12/2023'
	AND R_TR_DESC IN ('DDIS','ADIS','WPAY','UGAP','UWAR','DRSV','LTCA','0NF2','REPO',
					  'IMPO','GPSR','DHFL','PNM1','PNM2','PYNM','MNYG','WUQC','PYED',
					  'WSTU','CFPW','CFPM','PYC','PYAU','PYDL','PYED','PYBK','PYCO',
					  'BDR','AULW','GAPW','PYDU','DHBB', 'NSF') 

	--AND ISNULL(C.F0264_DEALER_HOLDBACK, 0) > '0'

ORDER BY 1


Select F0132_CROSS_KEY 'Account'
,F0264_DEALER_HOLDBACK 'Dealer Holdback'
from SHAW_EOD.dbo.DWR_RETAIL
where F0132_CROSS_KEY IN ('16843820002') and F0264_DEALER_HOLDBACK > '0'


--select left(a.F0132_CROSS_KEY, 7) 'Cross Key'
--,a.F0120_BORROWER_NAME 'Customer Name'
--,a.F0218_ORIGINAL_LOAN_AMOUNT 'Original Loan Amount'
--,a.F0145_LOAN_BALANCE 'Loan Balance'
--,a.F0233_ORIGINAL_TERM 'Original Term'
--,b.F0655_ORIGINAL_RATE 'Interest Rate'
--,a.F0198_PAYMENTS_PAID 'Payments Made'
--,a.F0148_LATE_CHARGES_DUE_AMOUNT 'Late Charges'
--,a.F0571_MISC_FEES_DUE_AMOUNT 'Misc Fee'
-- ,a.F0125_BORROWER_STATE 'State'
-- from SHAW_EOD.dbo.DWR_RETAIL a
-- left JOIN SHAW_EOD.dbo.DWR_RETAIL_WIDE b
--on a.F0132_CROSS_KEY = b.F0132_CROSS_KEY
-- left join shaw_eod.dbo.DWR_LEGAL c
--on a.F0132_CROSS_KEY = c.F0132_CROSS_KEY where left(a.F0132_CROSS_KEY, 7) in ('1709435')