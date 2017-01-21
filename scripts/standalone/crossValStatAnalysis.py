#!/usr/bin/env python


from time import time
start = time()

from RingerCore import ( csvStr2List, str_to_class, NotSet, BooleanStr
                       , Logger, LoggingLevel, emptyArgumentsPrintHelp )


from TuningTools.parsers import ( ArgumentParser, loggerParser,
                                  crossValStatsJobParser )

from TuningTools import ( CrossValidStatAnalysis, GridJobFilter, BenchmarkEfficiencyArchieve
                        , ReferenceBenchmark, ReferenceBenchmarkCollection )

parser = ArgumentParser( description = 'Retrieve performance information from the Cross-Validation method.'
                       , parents = [crossValStatsJobParser, loggerParser] )
parser.make_adjustments()

emptyArgumentsPrintHelp( parser )

## Retrieve parser args:
args = parser.parse_args( )
mainLogger = Logger.getModuleLogger(__name__)
mainLogger.level = args.output_level

if mainLogger.isEnabledFor( LoggingLevel.DEBUG ):
  import cProfile, pstats, StringIO
  pr = cProfile.Profile()
  pr.enable()

## Treat special arguments
# Check if binFilters is a class
if args.binFilters is not NotSet:
  try:
    args.binFilters = str_to_class( "TuningTools.CrossValidStat", args.binFilters )
  except (TypeError, AttributeError,):
    args.binFilters = csvStr2List( args.binFilters )

# Retrieve reference benchmark:
call_kw = {}
if args.refFile is not None:
  # If user has specified a reference performance file:
  mainLogger.info("Loading reference file...")
  effArchieve = BenchmarkEfficiencyArchieve.load(args.refFile, loadCrossEfficiencies = True)
  refBenchmarkCol = ReferenceBenchmarkCollection([])
  if args.operation is None:
    args.operation = effArchieve.operation
  from TuningTools.dataframe import RingerOperation
  args.operation = RingerOperation.retrieve(args.operation)
  refLabel = RingerOperation.branchName(args.operation)
  from itertools import product
  for etBin, etaBin in product( range( effArchieve.nEtBins if effArchieve.isEtDependent else 1 ),
                                range( effArchieve.nEtaBins if effArchieve.isEtaDependent else 1 )):
    # Make sure that operation is valid:
    benchmarks = (effArchieve.signalEfficiencies[refLabel][etBin][etaBin], 
                  effArchieve.backgroundEfficiencies[refLabel][etBin][etaBin])
    #try:
    #  crossBenchmarks = (effArchieve.signalCrossEfficiencies[refLabel][etBin][etaBin], 
    #                     effArchieve.backgroundCrossEfficiencies[refLabel][etBin][etaBin])
    #except KeyError, AttributeError:
    crossBenchmarks = (None, None)
    # Add the signal efficiency and background efficiency as goals to the
    # tuning wrapper:
    # FIXME: Shouldn't this be a function or class?
    opRefs = [ReferenceBenchmark.SP, ReferenceBenchmark.Pd, ReferenceBenchmark.Pf]
    refBenchmarkList = ReferenceBenchmarkCollection([])
    for ref in opRefs: 
      refArgs = []
      refArgs.extend( benchmarks )
      if crossBenchmarks is not None:
        refArgs.extend( crossBenchmarks )
      refBenchmarkList.append( ReferenceBenchmark( "OperationPoint_" + refLabel.replace('Accept','') + "_" 
                                                   + ReferenceBenchmark.tostring( ref ), 
                                                   ref, *refArgs ) )
    refBenchmarkCol.append( refBenchmarkList )
  del effArchieve
  call_kw['refBenchmarkCol'] = refBenchmarkCol

stat = CrossValidStatAnalysis( 
    args.discrFiles
    , binFilters = args.binFilters
    , binFilterIdxs = args.binFilterIdx
    , monitoringFileName = args.monitoringFileName
    , level = args.output_level
    )

stat(
    outputName     = args.outputFileBase
    , doMonitoring = args.doMonitoring
    , doCompress   = args.doCompress
    , toMatlab     = args.doMatlab
    , test         = args.test
    , **call_kw
    )

if mainLogger.isEnabledFor( LoggingLevel.DEBUG ):
  pr.disable()
  s = StringIO.StringIO()
  sortby = 'cumulative'
  ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
  ps.print_stats()
  print s.getvalue()
  end = time()
  mainLogger.debug("Job took %.2fs.", end - start)
