# MLOps Course Materials - September 2024

Welcome to the MLOps course repository for September 2024! This repository contains code and materials for running MLOps workflows on Jetstream2 cloud and NCSA Delta cluster and other places.

## Repository Structure

The repository is organized into two main folders:

1. `01_Jetstream2_DataPipelines`: Contains code for running data pipelines on Jetstream2 cloud.
2. `02_Delta_Multi_Node_Training`: Contains code for multi-node training on the NCSA Delta cluster.

## 01_Jetstream2_DataPipelines

This folder contains code for setting up and running data pipelines on Jetstream2 cloud. It includes:

- A Docker container for a Streamlit app that allows data upload
- Airflow configuration for orchestrating the Streamlit app and Label Studio for data annotation

### Getting Started with Jetstream2

1. Log in to Jetstream2:
   - Visit [https://docs.jetstream-cloud.org/ui/exo/login/](https://docs.jetstream-cloud.org/ui/exo/login/)
   - Follow the instructions to authenticate and access the Jetstream2 dashboard

2. Create a new instance:
   - In the Jetstream2 dashboard, navigate to "Instances"
   - Click "Launch Instance" and follow the prompts to set up your virtual machine
   - Choose an appropriate image and flavor based on your resource needs

3. Access your instance:
   - Once the instance is running, use SSH to connect to it (or use the webshell to connect)
   - Use the provided IP address and your SSH key

4. Set up the environment:
   - Clone this repository to your Jetstream2 instance
   - Navigate to the `01_Jetstream2_DataPipelines` directory
   - Follow the README in that directory for specific setup instructions

## 02_Delta_Multi_Node_Training

This folder contains code for running multi-node training jobs on the NCSA Delta cluster using SLURM.

### Getting Started with NCSA Delta

1. Log in to NCSA Delta:
   - Follow the instructions at [https://docs.ncsa.illinois.edu/systems/delta/en/latest/user_guide/login.html](https://docs.ncsa.illinois.edu/systems/delta/en/latest/user_guide/login.html)
   - You'll need to use SSH with your credentials to access the login nodes

2. Set up the environment:
   - Load Conda:
     ```
     module load anaconda3_gpu
     ```
   - Create a new Conda environment:
     ```
     conda create -n mlops python=3.8
     conda activate mlops
     ```

3. Clone the repository:
   - Use Git to clone this repository to your home directory on Delta

4. Navigate to the training code:
   ```
   cd mlops-sept-2024/02_Delta_Multi_Node_Training
   ```

5. Follow the README in that directory for specific instructions on submitting jobs and running multi-node training.

## Prerequisites

- Jetstream2 account and access (already given if requested in canvas)
- NCSA Delta account and access (already given if requested in canvas)
- Basic knowledge of Docker, Airflow, and SLURM (covered in the live sessions)
- Familiarity with Python and machine learning concepts

## Contributing

We welcome contributions to improve the course materials. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or concerns, please contact the course instructor or open an issue in this repository.

## Acknowledgments

- Translational AI Center at Iowa State University
- Jetstream2 cloud computing resource
- NCSA Delta supercomputing cluster
- All contributors and students of the MLOps course

Happy learning and experimenting with MLOps at scale!
