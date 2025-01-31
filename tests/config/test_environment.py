import pytest
import torch
from unittest.mock import patch
from config.environment import check_gpu_availability


def test_check_gpu_availability_cuda():
    with patch("torch.cuda.is_available", return_value=True):
        with patch("torch.tensor", return_value=torch.tensor([1.0], device="cuda")):
            assert check_gpu_availability() == "cuda"


def test_check_gpu_availability_cpu():
    with patch("torch.cuda.is_available", return_value=False):
        assert check_gpu_availability() == "cpu"


def test_check_gpu_availability_cuda_initialization_failure():
    with patch("torch.cuda.is_available", return_value=True):
        with patch("torch.tensor", side_effect=Exception("CUDA initialization failed")):
            assert check_gpu_availability() == "cpu"
