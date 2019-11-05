# Find matched unique kmers in contigs in parallel
# Author: Nicholas Cooley npc19@pitt.edu
###### -- libraries, data, and arguments --------------------------------------

# Arguments 1 == Queue / Val
# Arguments 2 == Sqlite file to generate / SqlFile
# Arguments 3 == Destination Folder / QueueFolder
# Arguments 4 == OverheadData / RDataInitial

Arguments <- commandArgs(trailingOnly = TRUE)

if (length(Arguments) != 4L) {
  stop("Incorrect Argument Number")
}

library(DECIPHER)

load(Arguments[4L],
     verbose = TRUE)

###### -- Generate a single synteny cell --------------------------------------

Queue <- as.integer(Arguments[1L])

Queue <- as.integer(Queue) + 1L

IDs <- JobMap[Queue, ]

Syn <- FindSynteny(dbFile = Arguments[2],
                   identifier = as.character(IDs),
                   verbose = TRUE)

Dist <- 1 - (2 * sum(Syn[[1, 2]][, "width"])) / sum(Syn[[1, 1]] + Syn[[2, 2]])

save(Dist,
     Syn,
     Queue,
     IDs,
     file = paste(Arguments[3],
                  formatC(x = Queue,
                          digits = 5,
                          flag = 0),
                  ".RData",
                  sep = ""))



