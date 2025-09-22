#!/usr/bin/env python3
"""
MLX-based AI client for homework grading
Optimized for Apple Silicon Mac
"""

import time
import streamlit as st
from typing import Optional, Dict, Any
import os

class MLXAIClient:
    """MLX-based AI client optimized for Apple Silicon"""
    
    def __init__(self, model_name: str = "lmstudio-community/gpt-oss-120b-MLX-8bit"):
        """Initialize MLX AI client
        
        Args:
            model_name: HuggingFace model name (MLX compatible)
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.model_loaded_in_memory = False
        self.last_response_time = None
        
        # Don't load model on initialization to avoid blocking UI
        # Model will be loaded on first use
    
    def _load_model(self):
        """Load the MLX model and tokenizer"""
        if self.model_loaded_in_memory:
            return  # Already loaded
            
        try:
            from mlx_lm import load, generate
            
            # Only show loading message if in Streamlit context
            if hasattr(st, 'info'):
                st.info(f"🔄 Loading {self.model_name} with MLX (optimized for Apple Silicon)...")
            
            # Load model and tokenizer
            self.model, self.tokenizer = load(self.model_name)
            self.model_loaded_in_memory = True
            
            if hasattr(st, 'success'):
                st.success(f"✅ {self.model_name} loaded successfully!")
            
        except Exception as e:
            self.model_loaded_in_memory = False
            if hasattr(st, 'error'):
                st.error(f"❌ Failed to load MLX model: {e}")
            else:
                print(f"❌ Failed to load MLX model: {e}")
    
    def is_available(self) -> bool:
        """Check if MLX AI is available"""
        try:
            import mlx_lm
            return True
        except ImportError:
            return False
    
    def generate_response(self, prompt: str, max_tokens: int = 2000, show_progress: bool = False) -> Optional[str]:
        """Generate response using MLX
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            show_progress: Show progress indicator
            
        Returns:
            Generated response or None if failed
        """
        if not self.model_loaded_in_memory:
            if show_progress:
                st.warning("Model not loaded, attempting to load...")
            self._load_model()
            
        if not self.model_loaded_in_memory:
            return None
        
        try:
            from mlx_lm import generate
            
            start_time = time.time()
            
            if show_progress:
                progress_bar = st.progress(0)
                status_text = st.empty()
                status_text.text("🚀 Generating response with MLX...")
            
            # Generate response
            response = generate(
                model=self.model,
                tokenizer=self.tokenizer,
                prompt=prompt,
                max_tokens=max_tokens,
                verbose=False
            )
            
            end_time = time.time()
            self.last_response_time = end_time - start_time
            
            if show_progress:
                progress_bar.progress(1.0)
                status_text.text(f"✅ Response generated in {self.last_response_time:.1f}s")
            
            return response
            
        except Exception as e:
            if show_progress:
                st.error(f"❌ MLX generation failed: {e}")
            return None
    
    def preload_model(self) -> bool:
        """Preload model into memory"""
        if not self.model_loaded_in_memory:
            self._load_model()
        return self.model_loaded_in_memory
    
    def check_model_memory_status(self) -> bool:
        """Check if model is loaded in memory (MLX compatibility method)"""
        return self.model_loaded_in_memory
    
    def _check_model_memory_status(self) -> bool:
        """Check if model is loaded in memory (internal method)"""
        return self.model_loaded_in_memory
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "name": self.model_name,
            "loaded": self.model_loaded_in_memory,
            "backend": "MLX (Apple Silicon optimized)",
            "last_response_time": self.last_response_time
        }

class LlamaCppClient:
    """Alternative llama.cpp client"""
    
    def __init__(self, model_path: str = None):
        """Initialize llama.cpp client
        
        Args:
            model_path: Path to GGUF model file
        """
        self.model_path = model_path
        self.model = None
        self.model_loaded_in_memory = False
        self.last_response_time = None
        
        if model_path and os.path.exists(model_path):
            self._load_model()
    
    def _load_model(self):
        """Load llama.cpp model"""
        try:
            from llama_cpp import Llama
            
            st.info(f"🔄 Loading model with llama.cpp...")
            
            # Load model with optimized settings for Mac
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=4096,  # Context window
                n_threads=8,  # Use multiple threads
                n_gpu_layers=-1,  # Use Metal if available
                verbose=False
            )
            
            self.model_loaded_in_memory = True
            st.success("✅ llama.cpp model loaded successfully!")
            
        except ImportError:
            st.error("❌ llama-cpp-python not installed. Run: pip install llama-cpp-python")
        except Exception as e:
            st.error(f"❌ Failed to load llama.cpp model: {e}")
            self.model_loaded_in_memory = False
    
    def is_available(self) -> bool:
        """Check if llama.cpp is available"""
        try:
            import llama_cpp
            return True
        except ImportError:
            return False
    
    def generate_response(self, prompt: str, max_tokens: int = 2000, show_progress: bool = False) -> Optional[str]:
        """Generate response using llama.cpp"""
        if not self.model_loaded_in_memory:
            return None
        
        try:
            start_time = time.time()
            
            if show_progress:
                progress_bar = st.progress(0)
                status_text = st.empty()
                status_text.text("🚀 Generating response with llama.cpp...")
            
            # Generate response
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=0.3,
                top_p=0.9,
                echo=False
            )
            
            end_time = time.time()
            self.last_response_time = end_time - start_time
            
            if show_progress:
                progress_bar.progress(1.0)
                status_text.text(f"✅ Response generated in {self.last_response_time:.1f}s")
            
            return response['choices'][0]['text']
            
        except Exception as e:
            if show_progress:
                st.error(f"❌ llama.cpp generation failed: {e}")
            return None

def get_available_ai_backends():
    """Get list of available AI backends"""
    backends = []
    
    # Check MLX
    mlx_client = MLXAIClient()
    if mlx_client.is_available():
        backends.append({
            "name": "MLX (Apple Silicon Optimized)",
            "type": "mlx",
            "recommended": True,
            "description": "Native Apple Silicon optimization, fastest on Mac"
        })
    
    # Check llama.cpp
    llamacpp_client = LlamaCppClient()
    if llamacpp_client.is_available():
        backends.append({
            "name": "llama.cpp",
            "type": "llamacpp", 
            "recommended": False,
            "description": "Cross-platform, requires GGUF model files"
        })
    
    # Check Ollama (existing)
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            backends.append({
                "name": "Ollama",
                "type": "ollama",
                "recommended": False,
                "description": "Local model server (currently having issues)"
            })
    except:
        pass
    
    return backends

def create_ai_client(backend_type: str = "mlx", **kwargs):
    """Factory function to create AI client"""
    if backend_type == "mlx":
        return MLXAIClient(**kwargs)
    elif backend_type == "llamacpp":
        return LlamaCppClient(**kwargs)
    elif backend_type == "ollama":
        # Import existing Ollama client
        from ai_grader import LocalAIClient
        return LocalAIClient(**kwargs)
    else:
        raise ValueError(f"Unknown backend type: {backend_type}")