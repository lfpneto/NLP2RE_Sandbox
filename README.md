# NLP2RE_Sandbox

This repository holds the code developed for the dissertation *Improving Change Impact Analysis of Requirements for Critical Systems Through Natural Language Processing*, FEUP 2024

## Dissertation Abstract

Machine learning has significantly impacted various domains by extracting meaningful patterns from large datasets, yet its integration into requirements engineering (RE) for safety-critical systems (SCS) presents unique challenges. This study offers a overview of the current research landscape and identifies promising directions for future work in the application Natural Language Processing (NLP) techniques to enhance RE tasks in the context of SCS. \newline

Starting by framing the interrelated nature of SCS  and the normative regulation, the research identifies untapped potential for usage of NLP methods. Particularly in case of SCS, we see efficiency potential in the development of tools for assistance in estimation effort and safety risks involved by introducing a change in SCS.\newline\newline

The goals of this research are categorized into three specific activities:

- Supporting Change-Impact Analysis (CIA).
- Tracing or eliciting safety-related aspects from existing norms and standards.
- Facilitating effective analysis, tracing and reuse of change to prevent safety risks and normative violations.

The study identifies research gaps in advancements in NLP techniques for semantic and discourse analysis, domain-specific word embedding models, human in the loop solutions and syntax-aware statement embedding that can benefit an automated retrieval of meaning for analysis of impact changes.\newline

Laying out the particular demands and constrains in SCS development, to answer the goals, this research addresses the identified constrains by exploring and outlining  NLP methods and tools in a specific pipeline to improve aspects of the RE process for CIA.

## Overview

This repository contains the implementation of a framework developed to enhance the analysis of change impact in requirements engineering (RE) for safety-critical systems (SCS) using Natural Language Processing (NLP) techniques.

## Table of Contents

- [Dissertation Abstract](#dissertation-abstract)
- [Overview](#overview)
- [Goals](#goals)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Framework Details](#framework-details)
- [Limitations and Future Work](#limitations-and-future-work)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Goals

- Supporting Change-Impact Analysis (CIA).
- Tracing or eliciting safety-related aspects from existing norms and standards.
- Facilitating effective analysis, tracing and reuse of change to prevent safety risks and normative violations.

Additionally, when evaluated to good results, the outcomes from topic modeling can be used as labels or attributes to train supervised models.

## Features

- Automated processing of .XML requierments datasets.
- Support for CIA by identifying topics of new requirements, relating to existing ones.
- Customizable proces flow (tokenization, stopword removal, stemming or lemmatization).
- Topic modeling using Latent Dirichlet Allocation (LDA) and Latent Semantic Analysis (LSA).
- Model report and evaluation metrics to assess performance.

## Installation

Before working with Conda, it’s always good practice to ensure that the latest version is installed. Open an Anaconda Prompt or terminal and enter:

0. **Clone the repository:**

    ```bash
    conda update conda --all
    conda update anaconda

To install and run this project using Anaconda, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/lfpneto/NLP2RE_Sandbox
    cd NLP2RE_Sandbox
    ```

2. **Create and activate a new conda environment:**

    ```bash
    conda env create -f environment.yml
    conda activate NLP2RE_Sandbox
    ```

3. **Install the required dependencies:**

    ```bash
    conda install --file requirements.txt
    ```

## Usage

To use the framework, follow these steps:

1. **Prepare your data:**
   - Your requirements documents, standards, and norms for model creation should be available in .XML format.
   - You can see examples for the .XML namespace in \data folder

2. **Configure the framework:**
   - Adjust the configuration parameters in the `config.json` for model creation.

3. **Run the topic modeling:**
   - Execute the main script to process your data and generate topic models.

    ```bash
    python .\src\main.py
    ```

4. **Evaluate the results:**
   - Use the resulting "evaluation_results_<Model_ID> to assess the performance of the model.

## Framework Details

The framework comprises the following components:

1. **Data Preprocessing:**
   - Tokenization
   - Stopword removal
   - Stemming and lemmatization

2. **Topic Modeling:**
   - LDA and LSA implementations using Gensim
   - Customizable parameters for model tuning

3. **Evaluation Metrics:**
   - Internal and external metrics to assess model performance
   - Resiter for human evaluation for practical applicability

![framework architecture](documentation\architecture.png)

## Limitations and Future Work

Limitations and opportunities for future enhancements:

- **Syntax-Aware Embeddings:** Combining syntax-aware embeddings and rule-based approaches for requierment syntax.
- **Metric Exploration:** Exploring more metrics.
- **Scalability:** The current pipeline does not foresee scalability.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please create an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact:

- Luis Neto
- GitHub: [lfneto](https://github.com/lfpneto)
