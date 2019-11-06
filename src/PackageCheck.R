# Check for packages, if not present install
# Author: Nicholas Cooley npc19@pitt.edu
###### -- libraries, data, and arguments --------------------------------------

if (!"BiocManager" %in% installed.packages()[, 1L]) {
  install.packages("BiocManager")
}

if (!"DECIPHER" %in% installed.packages()[, 1L]) {
  BiocManager::install("DECIPHER")
}