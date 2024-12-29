{ lib
, buildPythonPackage
, fetchFromGitHub
, pythonOlder
# build-system
, poetry-core
# runtime dependencies
, httpx
, python-dateutil
# dev dependencies
, black
, isort
, pre-commit
, pytest
, pytest-asyncio
, pytest-cov
, python-dotenv
, h2
# , sphinx
# , sphinx-press-theme
# , sphinx-toolbox
# , unasync-cli
}:

buildPythonPackage rec {
  pname = "storage3";
  version = "0.9.0";
  format = "pyproject";

  disabled = pythonOlder "3.9";

  src = fetchFromGitHub {
    owner = "supabase";
    repo = "storage-py";
    rev = "v${version}";
    hash = "sha256-Q/hE7ua7BzB/YbVAT5Ov25n9u91xQ7SBw5ikh1FXrU0="; # Replace with actual hash
  };

  nativeBuildInputs = [
    poetry-core
  ];

  propagatedBuildInputs = [
    httpx
    h2
    python-dateutil
  ];

  nativeCheckInputs = [
    black
    isort
    pre-commit
    pytest
    pytest-asyncio
    pytest-cov
    python-dotenv
    # sphinx
    # sphinx-press-theme
    # sphinx-toolbox
    # unasync-cli
  ];

  # Handle dependency version constraints

  pythonImportsCheck = [
    "storage3"
  ];

  doCheck = false;

  # Enable pytest-asyncio
  pytestFlagsArray = [ "--asyncio-mode=auto" ];

  meta = with lib; {
    description = "Supabase Storage client for Python";
    homepage = "https://supabase.github.io/storage-py";
    documentation = "https://supabase.github.io/storage-py";
    license = licenses.mit;
    maintainers = with maintainers; [ ]; # Add maintainers as needed
    classifiers = [
      "Programming Language :: Python :: 3"
      "License :: OSI Approved :: MIT License"
      "Operating System :: OS Independent"
    ];
  };
}