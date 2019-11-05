# Build Sqlite DB, and overhead data for parallelizing FindSynteny
# Author: Nicholas Cooley npc19@pitt.edu
###### -- libraries, data, and arguments --------------------------------------

# Argument 1 == FASTA file / SeqSet
# Argument 2 == Sqlite file to generate / SqlFile
# Argument 3 == Generate RData file / RDataInitial

Arguments <- commandArgs(trailingOnly = TRUE)

if (length(Arguments) != 3L) {
  stop("Incorrect Argument Number")
}

library(DECIPHER)

FNAs <- readDNAStringSet(filepath = Arguments[1])
FNANames <- names(FNAs)

###### -- construct large sqlite database -------------------------------------

DBPATH <- Arguments[2]

for (m1 in seq_along(FNAs)) {
  Seqs2DB(seqs = FNAs[m1],
          type = "XStringSet",
          dbFile = DBPATH,
          identifier = as.character(m1),
          verbose = TRUE)
}

JobMap <- matrix(data = list(),
                 nrow = length(FNAs),
                 ncol = length(FNAs))
JobDim <- dim(JobMap)

for (m1 in seq_len(length(FNAs) - 1L)) {
  for (m2 in (m1 + 1L):length(FNAs)) {
    JobMap[[m1, m2]] <- c(m1, m2)
  }
}

JobMap <- do.call(rbind,
                  JobMap[upper.tri(JobMap)])

save(JobMap,
     FNANames,
     JobDim,
     file = Arguments[3])



