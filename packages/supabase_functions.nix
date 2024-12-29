{
  lib,
  buildPythonPackage,
  fetchFromGitHub,
  pythonOlder,

  # build-system
  poetry-core,

  # dependencies
  httpx,
  strenum,

  # dev-dependencies
  black,
  isort,
  pre-commit,
  pyjwt,
  pytest,
  pytest-cov,
  # unasync-cli,
  pytest-asyncio,
  respx,
  setuptools,
  h2,
}:

buildPythonPackage rec {
  pname = "supafunc";
  version = "0.7.0";
  pyproject = true;

  disabled = pythonOlder "3.9";

  src = fetchFromGitHub {
    owner = "supabase";
    repo = "functions-py";
    rev = "refs/tags/v${version}";
                   
    hash = "sha256-oCzF8vFHzxxQ0hUEyz5Ueajt7ZpcFE058/ohQDjdvbU="; # Replace with the actual hash
  };

  build-system = [ poetry-core ];

  dependencies = [
    httpx
    h2
    strenum
  ];

  nativeBuildInputs = [
    black
    isort
    pre-commit
    setuptools
  ];

  nativeCheckInputs = [
    pyjwt
    pytest
    pytest-cov
    # unasync-cli
    pytest-asyncio
    respx
  ];

  pythonImportsCheck = [ "supabase_functions" ];

  postPatch = ''
    # Add alias logic to `src/a/__init__.py`
    mkdir -p src/supafunc
    echo 'from ..supabase_functions import *' > src/supafunc/__init__.py
  '';

  meta = with lib; {
    description = "Library for Supabase Functions";
    homepage = "https://github.com/supabase/functions-py";
    changelog = "https://github.com/supabase/functions-py/blob/v${version}/CHANGELOG.md";
    license = licenses.mit;
    maintainers = with maintainers; [ ris ];
  };
}
