{ lib
, buildPythonPackage
, fetchFromGitHub
, pythonOlder
# build-system
, poetry-core
# runtime dependencies
, websockets
, python-dateutil
, typing-extensions
, aiohttp
# dev dependencies
, black
, isort
, pre-commit
, pytest
, python-dotenv
, pytest-asyncio
, pytest-cov
}:

buildPythonPackage rec {
  pname = "realtime";
  version = "2.0.6";
  format = "pyproject";

  disabled = pythonOlder "3.9";

  src = fetchFromGitHub {
    owner = "supabase";
    repo = "realtime-py";
    rev = "v${version}";
    hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="; # Replace with actual hash
  };

  nativeBuildInputs = [
    poetry-core
  ];

  propagatedBuildInputs = [
    websockets
    python-dateutil
    typing-extensions
    aiohttp
  ];

  nativeCheckInputs = [
    pytest
    python-dotenv
    pytest-asyncio
    black
    isort
    pre-commit
    pytest-cov
  ];

  pythonImportsCheck = [
    "realtime"
  ];

  # Enable pytest-asyncio
  pytestFlagsArray = [ "--asyncio-mode=auto" ];

  meta = with lib; {
    description = "Supabase Realtime client for Python";
    homepage = "https://github.com/supabase/realtime-py";
    license = licenses.mit;
    maintainers = with maintainers; [ ]; # Add maintainers as needed
  };
}