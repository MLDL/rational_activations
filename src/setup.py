import glob
from pathlib import Path
import airspeed
from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
from torch.cuda import is_available as torch_cuda_available
# degrees
#degrees = [(3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (5, 4)]
degrees = [(5, 4)]
degrees = [(5, 4), (7, 6)]


def generate_cpp_module(fname, degrees=degrees, versions=None):
    file_content = airspeed.Template("""
\#include <torch/extension.h>
\#include <vector>
\#include <iostream>

#define CHECK_CUDA(x) TORCH_CHECK(x.is_cuda(), #x " must be a CUDA tensor")
#define CHECK_CONTIGUOUS(x) TORCH_CHECK(x.is_contiguous(), #x " must be contiguous")
#define CHECK_INPUT(x) CHECK_CUDA(x); CHECK_CONTIGUOUS(x)


#foreach ($vname in $versions)
#if( $vname == 'D' )
#set ($forward_header = 'const bool training, const unsigned long long iteration, torch::Tensor x, torch::Tensor n, torch::Tensor d')
#set ($backward_header = 'const bool training, const unsigned long long iteration, torch::Tensor grad_output, torch::Tensor x, torch::Tensor n, torch::Tensor d')
#set ($forward_invocation = 'training, iteration, x, n, d')
#set ($backward_invocation = 'training, iteration, grad_output, x, n, d')
#else
#set ($forward_header = 'torch::Tensor x, torch::Tensor n, torch::Tensor d')
#set ($backward_header = 'torch::Tensor grad_output, torch::Tensor x, torch::Tensor n, torch::Tensor d')
#set ($forward_invocation = 'x, n, d')
#set ($backward_invocation = 'grad_output, x, n, d')
#end
    #foreach ($degs in $degrees)
	at::Tensor pau_cuda_forward_${vname}_$degs[0]_$degs[1]($forward_header);
    std::vector<torch::Tensor> pau_cuda_backward_${vname}_$degs[0]_$degs[1]($backward_header);
    #end


    #foreach ($degs in $degrees)
    at::Tensor pau_forward_${vname}_$degs[0]_$degs[1]($forward_header) {
        CHECK_INPUT(x);
        CHECK_INPUT(n);
        CHECK_INPUT(d);

        return pau_cuda_forward_${vname}_$degs[0]_$degs[1]($forward_invocation);
    }
    std::vector<torch::Tensor> pau_backward_${vname}_$degs[0]_$degs[1]($backward_header) {
        CHECK_INPUT(grad_output);
        CHECK_INPUT(x);
        CHECK_INPUT(n);
        CHECK_INPUT(d);

        return pau_cuda_backward_${vname}_$degs[0]_$degs[1]($backward_invocation);
    }
    #end
#end

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
#foreach ($degs in $degrees)
    #foreach ($vname in $versions)
    m.def("forward_${vname}_$degs[0]_$degs[1]", &pau_forward_${vname}_$degs[0]_$degs[1], "PAU forward ${vname}_$degs[0]_$degs[1]");
    m.def("backward_${vname}_$degs[0]_$degs[1]", &pau_backward_${vname}_$degs[0]_$degs[1], "PAU backward ${vname}_$degs[0]_$degs[1]");
    #end
#end
}
    """)

    content = file_content.merge(locals())

    with open(fname, "w") as text_file:
        text_file.write(content)


def generate_cpp_kernels_module(fname, degrees=degrees, template_contents=None):
    degrees = [[e[0], e[1], max(e[0], e[1])] for e in degrees]

    template = """
\#include <torch/extension.h>
\#include <ATen/cuda/CUDAContext.h>
\#include <cuda.h>
\#include <cuda_runtime.h>
\#include <vector>
\#include <stdlib.h>

\#include <curand.h>
\#include <curand_kernel.h>
\#include <curand_philox4x32_x.h>

constexpr uint32_t THREADS_PER_BLOCK = 512;
"""


    file_content = airspeed.Template(template + template_contents)

    content = file_content.merge(locals())

    with open(fname, "w") as text_file:
        text_file.write(content)

if torch_cuda_available():
    version_names = []
    template_contents = ""
    for template_fname in sorted(glob.glob("cuda/versions/*.cu")):
        version_names.append(Path(template_fname).stem)
        with open(template_fname) as infile:
            template_contents += infile.read()

    generate_cpp_module(fname='cuda/pau_cuda.cpp', versions=version_names)
    generate_cpp_kernels_module(fname='cuda/pau_cuda_kernels.cu', template_contents=template_contents)


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setup(
    name='pau',
    version='0.0.16',
    author="Alejandro Molina, Quentin Delfosse, Patrick Schramowski",
    author_email="molina@cs.tu-darmstadt.de, quentin.delfosse@cs.tu-darmstadt.de",
    description="Pade Activation Unit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ml-research/pau",
    packages=find_packages(),
    package_data={'': ['*.json']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License"
    ],
    install_requires=requirements,
    ext_modules=[
        CUDAExtension('pau_cuda', [
            'cuda/pau_cuda.cpp',
            'cuda/pau_cuda_kernels.cu',
        ],
        extra_compile_args={'cxx': [],
            'nvcc': ['-gencode=arch=compute_60,code="sm_60,compute_60"', '-lineinfo']
        }
    ),
    ] if torch_cuda_available() else [],
    cmdclass={
        'build_ext': BuildExtension
    },
    setup_requires=['airspeed', 'numpy', 'torch', 'scipy'],
    python_requires='>=3.5.0')
