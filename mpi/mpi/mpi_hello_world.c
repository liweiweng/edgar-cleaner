// Tutorial MPI program - Texas Tech University HPCC
//
// An intro MPI hello world program that uses MPI_Init, MPI_Comm_size,
// MPI_Comm_rank, MPI_Finalize, and MPI_Get_processor_name.
//
#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
  int world_size;				//The number of processes that were spawned.
  int world_rank;				//The rank of the current process.
  char processor_name[MPI_MAX_PROCESSOR_NAME];	//The name of the current process
  int name_len;					//The length of the current processes' name.


  // Initialize the MPI environment.
  MPI_Init(NULL, NULL);

  // Get and set the number of processes
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);

  // Get and set the rank of the process
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

  // Get and set the name and length of the processor
  MPI_Get_processor_name(processor_name, &name_len);

  // Print off a hello world message
  printf("Hello world from processor %s, rank %d out of %d processors\n",
         processor_name, world_rank, world_size);

  // Finalize the MPI environment. No more MPI calls can be made after this
  MPI_Finalize();
}
