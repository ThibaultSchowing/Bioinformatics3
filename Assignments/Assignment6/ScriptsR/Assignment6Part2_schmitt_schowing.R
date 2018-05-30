print("Assignment 6 - Schmitt Schowing")




source("http://bioconductor.org/biocLite.R")
biocLite("impute")
biocLite("samr")

biocLite("preprocessCore")
library(preprocessCore)
library(samr)


mydata = read.csv('./ms_data.txt', sep = '\t')
df <- as.data.frame(mydata, col.names = mydata[1,], cut.names = FALSE)

#dim(df)
#names(df)
#str(df)


df.transformed <- df

df.transformed[, 1:9] <- log(df[1:9], 2)

# Normalization - extract matrix and replace
df.quantile_normalized <-df.transformed
x = data.matrix(df.transformed[,1:9])
x <- normalize.quantiles(x)


df.quantile_normalized[,1:9] <- x

# Differential expression analysis
x <- subset(df.quantile_normalized, select=c("control.1","control.2", "control.3", "rna1.1", "rna1.2", "rna1.3"))
x2 <- subset(df.quantile_normalized, select=c("control.1","control.2", "control.3", "rna2.1", "rna2.2", "rna2.3"))

x <- as.matrix(x)
x <- t(x)

x2 <- as.matrix(x2)
x2 <- t(x2)

y <- subset(df["Gene.names"])
y <- as.matrix(y)
y <- as.matrix(y)

dim(y)


dim(x)


# 
df.analysis1 <- SAM(x,y = c(1,1,1,2,2,2) ,
                   resp.type=c("Two class unpaired"),
                   genenames = df$Gene.names,
                   s0=NULL,
                   s0.perc=NULL,
                   nperms=100,
                   center.arrays=FALSE,
                   regression.method=c("standard","ranks"),
                   knn.neighbors=10,
                   random.seed=NULL,
                   logged2 = TRUE,
                   fdr.output = 0.20,
                   eigengene.number = 1)

df.analysis2 <- SAM(x2,y = c(1,1,1,2,2,2) ,
                    resp.type=c("Two class unpaired"),
                    genenames = df$Gene.names,
                    s0=NULL,
                    s0.perc=NULL,
                    nperms=100,
                    center.arrays=FALSE,
                    regression.method=c("standard","ranks"),
                    knn.neighbors=10,
                    random.seed=NULL,
                    logged2 = TRUE,
                    fdr.output = 0.20,
                    eigengene.number = 1)

summary(df.analysis1)

# "rna2.1", "rna2.2", "rna2.3"
