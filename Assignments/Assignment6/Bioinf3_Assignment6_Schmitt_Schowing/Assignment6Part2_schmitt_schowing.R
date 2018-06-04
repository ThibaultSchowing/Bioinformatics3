print("Assignment 6 - Schmitt Schowing")

# Install the packages

#source("http://bioconductor.org/biocLite.R")
#biocLite("impute")
#biocLite("samr")
#biocLite("preprocessCore")

library(preprocessCore)
library(samr)

# Reade the data
mydata = read.csv('./ms_data.txt', sep = '\t')
df <- as.data.frame(mydata, col.names = mydata[1,], cut.names = FALSE)

#dim(df)
#names(df)
#str(df)

# Log-transformation of the data part
df.transformed <- df
df.transformed[, 1:9] <- log(df[1:9], 2)

# Normalization - extract matrix and replace
df.quantile_normalized <-df.transformed
x = data.matrix(df.transformed[,1:9])
x <- normalize.quantiles(x)


df.quantile_normalized[,1:9] <- x

# Differential expression analysis - two sets:

x <- subset(df.quantile_normalized, select=c("control.1","control.2", "control.3", "rna1.1", "rna1.2", "rna1.3"))
x2 <- subset(df.quantile_normalized, select=c("control.1","control.2", "control.3", "rna2.1", "rna2.2", "rna2.3"))

x <- as.matrix(x)
x2 <- as.matrix(x2)


# First experiment (with first set of rna)
# Run once and plot the results

df.analysis1 <- SAM(x,y = c(1,1,1,2,2,2) ,
                   resp.type=c("Two class unpaired"),
                   genenames = df[["Gene.names"]],
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

# Plot the result:
plot(df.analysis1)

# Delta cutoff
df.analysis1$del

# Other informations
summary(df.analysis1)

# Tables we're looking for: genes.up and .low. Here we have some number and size
df.analysis1$siggenes.table

# Let's do it with a variation of the parameters fdr.output and nperms and write the results to a file.
# NOTE: depending if the set x or x2 were used, the filename has to be changed manually.

# Open file for output
fileConn<-file("outputSAMx2.txt", "w")

write(c("Assignment 6 - SAM function output with variating fdr.output and nperms"), fileConn, append = TRUE)

# Varies the fdr.output parameter from 0.1 to 1 with a 0.1 increment
# varies the nperms parameter from 100 to 1000 witn a 100 increment

for(i in 1:10){
  for(j in 1:10){
    fdr = 0.1 * i 
    per = 100 * j
    
    line = "\n\n"
    write(line, fileConn, append = TRUE)
    
    line = paste(c("fdr.output", fdr), collapse = " ")
    write(line, fileConn, append = TRUE)
    
    line = paste(c("nperms", per), collapse = " ")
    write(line, fileConn, append = TRUE)
    
    #NOTE: here passing the gene names didn't work. No idea why. 
    
    
    df.analysis1 <- SAM(x2,y = c(1,1,1,2,2,2) ,
                        resp.type=c("Two class unpaired"),
                        genenames = NULL,
                        s0=NULL,
                        s0.perc=NULL,
                        nperms=per,
                        center.arrays=FALSE,
                        regression.method=c("standard","ranks"),
                        knn.neighbors=10,
                        random.seed=NULL,
                        logged2 = TRUE,
                        fdr.output = fdr,
                        eigengene.number = 1)
    
    line = "\nUp-Regulated protein\n"
    write(line, fileConn, append = TRUE)
    write.table(df.analysis1$siggenes.table$genes.up, file = fileConn, append = TRUE, quote = TRUE, sep = " ",
                eol = "\n", na = "NA", dec = ".", row.names = TRUE,
                col.names = TRUE, qmethod = c("escape", "double"),
                fileEncoding = "")
    line = "\nDown-Regulated protein\n"
    write(line, fileConn, append = TRUE)
    write.table(df.analysis1$siggenes.table$genes.lo, file = fileConn, append = TRUE, quote = TRUE, sep = " ",
                eol = "\n", na = "NA", dec = ".", row.names = TRUE,
                col.names = TRUE, qmethod = c("escape", "double"),
                fileEncoding = "")
  }
  
}

# Close file
close(fileConn)

df.analysis1$siggenes.table$genes.up
df.analysis1$del


# From the tables, we get the following row 
df[3004,]
df[2083,]
df[477,]
df[3861,]
df[1790,]
df[2376,]
df[898,]
df[3332,]
df[1428,]
df[5246,]

# And the downs
df[2018,]
df[3162,]
df[3325,]
df[1669,]
df[3026,]
df[868,]
df[4009,]
df[3264,]
df[309,]
df[1051,]




