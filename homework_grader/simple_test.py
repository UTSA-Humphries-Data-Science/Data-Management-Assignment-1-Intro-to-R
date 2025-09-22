#!/usr/bin/env python3
"""
Super simple MLX test - just see if it works
"""

print("🔍 Simple MLX Test")
print("=" * 30)

print("Step 1: Checking if MLX is installed...")
try:
    import mlx_lm
    print("✅ MLX is installed")
except ImportError:
    print("❌ MLX not installed")
    exit(1)

print("\nStep 2: Checking cache directory...")
from pathlib import Path
cache_dir = Path.home() / ".cache" / "huggingface"
print(f"Cache location: {cache_dir}")
print(f"Cache exists: {cache_dir.exists()}")

if cache_dir.exists():
    total_size = sum(f.stat().st_size for f in cache_dir.rglob('*') if f.is_file())
    size_gb = total_size / (1024**3)
    print(f"Current cache size: {size_gb:.1f}GB")

print("\nStep 3: Testing with tiny model...")
print("This should download ~500MB and be very fast...")

try:
    from mlx_lm import load
    
    # Use the smallest possible model
    tiny_model = "mlx-community/Llama-3.2-1B-Instruct-4bit"
    
    print(f"Loading: {tiny_model}")
    print("(If this is the first time, it will download)")
    
    import time
    start = time.time()
    
    model, tokenizer = load(tiny_model)
    
    elapsed = time.time() - start
    print(f"✅ Loaded in {elapsed:.1f} seconds")
    
    # Test it
    print("\nStep 4: Testing generation...")
    from mlx_lm import generate
    
    response = generate(model, tokenizer, "Hello", max_tokens=3, verbose=False)
    print(f"✅ Response: '{response}'")
    
    print(f"\n🎉 SUCCESS! MLX is working perfectly.")
    print(f"Ready to download your homework grading models.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Something went wrong with MLX")