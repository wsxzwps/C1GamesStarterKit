$scriptPath = Split-Path -parent $PSCommandPath;
$algoPath = "$scriptPath\algo_strategy_dynamic_defence.py"

py -3 $algoPath
