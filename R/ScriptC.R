# Collapse parallel output into a single distance matrix
# a single names txt
# and a single rdata file
# Author: Nicholas Cooley npc19@pitt.edu
###### -- libraries, data, and arguments --------------------------------------

# Argument 1 == Folder location of parallel outputs / QueueFolder
# Argument 2 == DistanceMatrix output / DistOut
# Argument 3 == SeqNames output / NamesOut
# Argument 4 == RData file output / FinalRData

Arguments <- commandArgs(trailingOnly = TRUE)

if (length(Arguments) != 4L) {
  stop("Incorrect Argument Number.")
}

library(DECIPHER)

FileList <- list.files(Arguments[1L])
load(Arguments[4L],
     verbose = TRUE)

DistMat <- matrix(data = 0,
                  nrow = JobDim[1L],
                  ncol = JobDim[2L])

dimnames(DistMat) <- list(seq(nrow(DistMat)),
                          seq(nrow(DistMat)))

pBar <- txtProgressBar(style = 3L)

for (m1 in seq_along(FileList)) {
  load(FileList[m1],
       verbose = FALSE)
  DistMat[IDs[1L], IDs[2L]] <- DistMat[IDs[2L], IDs[1L]] <- Dist
  setTxtProgressBar(pb = pBar,
                    value = m1 / length(FileList))
}

NamesOut <- paste(seq(length(FNANames)),
                  FNANames,
                  sep = "_")

write.table(DistMat,
            file = Arguments[2L],
            append = FALSE,
            quote = FALSE)

writeLines(NamesOut,
           Arguments[3L])

save(DistMat,
     NamesOut,
     file = Arguments[4L],
     compress = "xz")



