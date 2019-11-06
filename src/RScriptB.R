# Find matched unique kmers in contigs in parallel
# Author: Nicholas Cooley npc19@pitt.edu
###### -- libraries, data, and arguments --------------------------------------

# no longer valid arguments
# Arguments 1 == Queue / Val
# Arguments 2 == Sqlite file to generate / SqlFile
# Arguments 3 == Destination Folder / QueueFolder
# Arguments 4 == OverheadData / RDataInitial

Arguments <- commandArgs(trailingOnly = TRUE)

suppressMessages(library(DECIPHER))

load(paste(Arguments[2L],
           "/",
           "Initial.RData",
           sep = ""),
     verbose = FALSE)

###### -- Generate a single synteny cell --------------------------------------

Queue <- as.integer(Arguments[1L])

# print(Queue)

IDs <- JobMap[Queue, ]

Syn <- FindSynteny(dbFile = paste(Arguments[2L],
                                  "/",
                                  "DBPATH.sqlite",
                                  sep = ""),
                   identifier = as.character(IDs),
                   verbose = FALSE)

Dist <- 1 - (2 * sum(Syn[[1, 2]][, "width"])) / sum(Syn[[1, 1]] + Syn[[2, 2]])

save(Dist,
     Syn,
     Queue,
     IDs,
     file = paste(Arguments[3L],
                  "/",
                  formatC(x = Queue,
                          digits = 5,
                          flag = 0),
                  ".RData",
                  sep = ""))



