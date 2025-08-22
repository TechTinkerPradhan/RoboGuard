# Roboguard

[Safety Guardrail for LLM-Enabled Robots](https://robo-guard.github.io/).

## Installation


Install the following dependencies 

- [spot](https://spot.lre.epita.fr/) LTL library
- [SPINE](https://github.com/KumarRobotics/SPINE)

Then install this repo:

```sh
# if installing a local copy, skip this step
git clone git@github.com:ZacRavichandran/roboguard.git  

cd roboguard
python -m pip install -e .[examples]
```



## Roboguard Example

The provided [example](./scripts/example.md) demonstrates RoboGuard on a few malicious and benign plans.

You will need to configure an OpenAI API key (please see their [documentation](https://openai.com/index/openai-api/)).

To run, converted the provided markdown file to a jupyter notebook

```sh
cd ./examples
jupytext --to ipynb example.md  -o example.ipynb
```

## Experiment Pipeline

To reproduce the evaluation pipeline locally, follow these steps:

1. **Install dependencies**: Ensure you have Python 3.8+ and install required packages:

   ```bash
   git clone git@github.com:TechTinkerPradhan/RoboGuard.git
   cd RoboGuard
   pip install spot
   pip install -e .[examples]
      ```
   pip install git+https://github.com/KumarRobotics/SPINE.git
      ```
   ``````

3. **Create a dataset**: Use `scripts/create_dataset.py` to generate a CSV of labelled instructions:

   ```bash
   python scripts/create_dataset.py --output data/experiment_scenarios.csv
      ```
   ```

4. **Run experiments**: Use `scripts/run_experiments.py` specifying your dataset, scene graph, safety mode and result file:

   ```bash
   python scripts/run_experiments.py --dataset data/experiment_scenarios.csv --graph data/perch_small.json --mode combined --output results_combined.csv
      ```
   ```

5. **Evaluate results**: Compute metrics from the results CSV with `scripts/evaluate_results.py`:

   ```bash
   python scripts/evaluate_results.py --input results_combined.csv
      ```
   ```

These steps will generate results for different safety modes and compute unsafe acceptance and success rates.

The notebook includes a simple semantic graph, ruleset, and candidate plans.
RoboGuard will generate specifications given the semantic graph and ruleset, and then it will evaluate the plans given the specifications.

You can also generate plans with the provided LLM-enabled planner.


## Running with an LLM-enabled planner 

We evaluate RoboGuard when running on top of the [SPINE](https://zacravichandran.github.io/SPINE/) LLM-enabled planner. 
While SPINE is agnostic to the specific robot platform, we use a Cleapath Jackal with the following configuration
- Intel Realsense 
- Ouster OS1
- Nvidia RTX 4000 
- Ryzen 4 3600




## Citation

If you find this helpful, please cite 

```
@article{ravichandran_roboguard,
  title={Safety Guardrails for LLM-enabled Robots},: 
  author={Zachary Ravichandran and Alexander Robey and Vijay Kumar and George J. Pappas and Hamed Hassani},
  year={2025},
  journal={arXiv preprint arXiv:2503.07885},
  url={https://arxiv.org/abs/2503.07885}
}
```
