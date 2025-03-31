# MatplotAlt

MatplotAlt is a Python library for generating and displaying matplotlib figure alt text in computational notebooks.

This is an ongoing project, so let us know if you have any feedback or feature requests on our [discussion page](https://github.com/make4all/matplotalt/discussions)! To see more examples and evaluation of our methods, see our [preprint](https://arxiv.org/abs/2503.20089).

## Installation

The latest release can be installed from PyPI:

``` pip install matplotalt ```

## Usage

Documentation is available at [matplotalt's read-the-docs page](https://matplotalt.readthedocs.io), including [examples](https://matplotalt.readthedocs.io/en/latest/notebooks/examples.html), [API reference](https://matplotalt.readthedocs.io/en/latest/api.html), and other useful information.

MatplotAlt's ``show_with_alt`` function can generate and display alt text for a figure in a single line of code. **Note**: ``show_with_alt`` is meant to replace ``plt.show`` and will not work if Matplotlib's ``show`` is called first.

```
import matplotlib.pyplot as plt
from matplotalt import show_with_alt

sunshine_hours = [69, 108, 178, 207, 253, 268, \
                  312, 281, 221, 142, 72, 52]
months = ["Jan", "Feb", "Mar", "Apr", "May", "June", \
          "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
plt.title("Monthly Sunshine in Seattle")
plt.barh(list(range(12)), sunshine_hours)
plt.xlabel("Average hours of sunlight")
plt.ylabel("Month")
plt.yticks(ticks=list(range(12)), labels=months)

show_with_alt(desc_level=3, methods="markdown")
```

The ``desc_level`` parameter controls how detailed the description is from 1 (least detail) to 3 (most) based on [Lundgard and Satyanarayan, 2021](https://arxiv.org/pdf/2110.04406).

The ``methods`` parameter controls how to display generated alt text and accepts one or a list of strings. Currently supported methods to display alt text are:

* __html__: displays the last figure in html with an alt property containing the alt text.
* __markdown__: display text in markdown in the current cell output.
* __new_cell__: create a new (code) cell after this one containing the alt text.
* __txt_file__: writes the alt text to a text file.
* __img_file__: saves the last matplotlib figure with the generated description in its alt property.

If you need more control over how alt text is created or displayed, we also provide the ``generate_alt_text`` function, which returns a description for the figure as a string, and ``add_alt_text``, which displays a given string using any of the supported methods.


There are also "API" versions of each function (``show_with_api_alt``, ``generate_api_alt_text``) which generate alt text using a LLM through OpenAI and Azure APIs.

## alttextify

MatplotAlt provides the ``alttextify`` command to automatically add alt text to each matplotlib figure in a IPython notebook with the same options as ``show_with_alt``. For example,

```
alttextify ./examples/examples_no_alt.ipynb examples_with_alt -s html
```

will add alt text to each figure in the examples_no_alt.ipynb notebook through the HTML alt property without changing any of the code cells. ``alttextify`` can also be used to generate alt texts with LLMs:

```
alttextify ./examples/examples_no_alt.ipynb examples_with_llm_alt -k <your API key> -m gpt-4-vision-preview -us
```

## Attribution

If you use the datasets or code provided with this work, consider citing it as below:
```
@article{nylund2025matplotalt,
  title={MatplotAlt: A Python Library for Adding Alt Text to Matplotlib Figures in Computational Notebooks},
  author={Nylund, Kai and Mankoff, Jennifer and Potluri, Venkatesh},
  journal={arXiv preprint arXiv:2503.20089},
  year={2025}
}
```