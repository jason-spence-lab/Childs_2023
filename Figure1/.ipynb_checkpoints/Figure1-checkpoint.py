'''
BASIC SINGLE CELL ANALYSIS SCRIPT
by Josh Wu
4 June, 2019

USE THIS ONE 

Relies heavily on the Scanpy Python module developed by the Theis Lab
Read more about Scanpy at https://scanpy.readthedocs.io/en/latest/index.html

Contains analysis of kidney samples obtained by Emily Holloway
Template for a Basic Analysis 

In progress ---
Moving to encapsulate parameters and relevant functions using class sca_set()
'''

from sca_run import *
#from tools.pipelines import *

figdir = '/Users/charliechilds/SpenceLab/EREGHIO_singlenuc/Figures/'
an_run = sca_run()
#############################################################################
## Change this to point toward your mount location for our MiStorage share ##
#############################################################################
an_run.storage_mount_point = '/Volumes/umms-spencejr/'

## IDs of samples as represented in the metadata table
an_run.sample_list = ['7868-1']


## List of interesting genes
an_run.add_gene_list(markers=['S100B','PLP1','STMN2','ELAVL4','CDH5','KDR','ECSCR','CLDN5','COL1A1','COL1A2','DCN','ACTA2','TAGLN','ACTG2','MYLK','EPCAM','CDH1','CDX2','CLDN4','PTPRC','HLA-DRA','ARHGDIB','CORO1A','MKI67','TOP2A'],
					 label='basic_list')

# an_run.add_gene_list(markers=['CDH5','KDR','ECSCR','CLDN5','CD31','NG2','PDGFRB','CD146','NES','DES',],
# 					 label='ec_peri_list')

# an_run.add_gene_list(markers=['CDX2','LGR5','OLFM4','TFF1','FABP2','ALPI','RBP2','BEST4','TFF1','SPIB','MUC2','SPDEF','DLL1','TRPM5','TAS1R3','CHGA','NEUROD1','PAX6','ARX','REG4','DEFA5','REG3A'],
# 					 label='publicationCSC_epithelial_list')

# # an_run.add_gene_list(markers= ['EGF','NRG1','NRG2','NRG3','NRG4','TGFA','HBEGF','AREG','BTC','EPGN','EREG','EGFR','ERBB2','ERBB3','ERBB4'],
# # 					 label='EGF_list')

# an_run.add_gene_list(markers= ['LGR5','OLFM4','FABP2','SI','DPP4','EGF','NRG1','NRG2','NRG3','NRG4','TGFA','HBEGF','AREG','BTC','EPGN','EREG','EGFR','ERBB2','ERBB3','ERBB4'],
# 					 label='ISC_SUBEPI_EGF_list')

# an_run.add_gene_list(markers= ['CDX2','SOX2','P63','INS','AMY2B','PDX1','MUC5AC','TFF2','SOX10','FOXJ1','NKX2-1'],
# 					 label='offtarget_list')

# an_run.add_gene_list(markers= ['F3','NRG1','DLL1','PDGFRA','BMP3','NPY'],
# 					 label='SEC_list')

# an_run.add_gene_list(markers= ['WT1', 'UPK3B', 'KRT19', 'PDPN'],
# 					 label='SEC_list')

# an_run.add_gene_list(markers= ['RUNX1','NOS','TUBB3', 'S100B', 'GDNF', 'EDN3', 'KIT', 'TH', 'CALB1', 'CALB2', 'CHAT', '5-HT', 'PHOX2A','PHOX2B', 'ASCL1','EDNRB'],
# 					 label='neuronalcelltypes_list')

## Parameters used to filter the data - Mainly used to get rid of bad cells
an_run.set_filter_params(min_cells = 0, # Filter out cells 
						 min_genes = 1200, # Filter out cells with fewer genes to remove dead cells
						 max_genes = 6000, # Filter out cells with more genes to remove most doublets
						 max_counts = 17500, # Filter out cells with more UMIs to catch a few remaining doublets
						 max_mito = 0.1) # Filter out cells with high mitochondrial gene content

## Parameters used for initial clustering analysis
an_run.set_analysis_params(n_neighbors = 15, # Size of the local neighborhood used for manifold approximation
						   n_pcs = 18, # Number of principle components to use in construction of neighborhood graph
						   spread = 1, # In combination with min_dist determines how clumped embedded points are
						   min_dist = 0.4, # Minimum distance between points on the umap graph
						   resolution = 0.5) # High resolution attempts to increases # of clusters identified

an_run.set_plot_params(size=10, final_quality = True)



## Basic pipeline for analysis - will filter data, process, cluster, etc. and output relevant figures
an_run.pipe_basic(figdir)

## If you find some interesting clusters that you want to "zoom in" on and recluster, you can use the following code

#New analysis parameters for the subset of parameters
# analysis_params_ext = dict(n_neighbors = 15,
# 						n_pcs = 18,
# 						spread = 1,
# 						min_dist = 0.4,
# 						resolution = 0.94)

# an_run.pipe_ext(analysis_params_ext, figdir=figdir, extracted=['0','2','3','4','5','6','7','8'], load_save='adata_save.p')

# analysis_params_ext = dict(n_neighbors = 9,
# 						n_pcs = 9,
# 						spread = 1,
# 						min_dist = 0.4,
# 						resolution = 0.5)

# an_run.pipe_ext(analysis_params_ext, figdir=figdir, extracted=['0','1','2','3','4','5','6','7','8','9','10'], load_save='/extracted/adata_save.p')


#### Exporting data for ligand-receptor pairing analysis
# # Export cluster metadata
# run_save = pickle.load(open(''.join([figdir,'adata_save.p']),"rb"))
# adata = run_save.adata.copy()
# df_meta = pd.DataFrame(data=[])
# os.makedirs(os.path.dirname(''.join([figdir,'data_csvs/'])), exist_ok=True) 
# adata.obs.loc[:,['louvain']].to_csv(''.join([figdir,'data_csvs/metadata.csv']))
# ## Export raw counts file
# adata_postfiltered = run_save.adata_postFiltered.copy()
# # sc.pp.normalize_total(adata_postfiltered)#,target_sum=10000)
# adata_raw =adata.raw.copy()
# print(adata_raw)
# df = pd.DataFrame(adata_raw.X.T.toarray())
# df.columns = adata_postfiltered.obs.index
# df.set_index(adata_postfiltered.var.index, inplace=True) 
# print(df)
# df.to_csv(''.join([figdir,'/data_csvs/counts.csv']))
#cellphonedb method statistical_analysis /Users/lushu/Desktop/cellphoneDB/cellphonedb_meta.txt /Users/lushu/Desktop/cellphoneDB/cellphonedb_count.txt --counts-data=gene_name