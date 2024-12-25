{
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachSystem [ "x86_64-linux" "aarch64-linux" ] (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python3 = pkgs.python3;

        pyproject = builtins.fromTOML (builtins.readFile ./pyproject.toml);

        pname = pyproject.project.name or "unknown-package";
        version = pyproject.project.version or "0.1.0";

        pkg = python3.pkgs.buildPythonPackage rec {
          inherit pname version;
          format = "pyproject";
          src = ./.;

          nativeBuildInputs = with python3.pkgs; [ setuptools ];

          propagatedBuildInputs = with python3.pkgs; [
            numba
            pillow
            numpy
            scikit-learn
          ];
        };

        editablePkg = pkg.overrideAttrs (oldAttrs: {
          nativeBuildInputs = oldAttrs.nativeBuildInputs ++ [
            (python3.pkgs.mkPythonEditablePackage {
              pname = pname;
              scripts = pyproject.project.scripts or {};
              version = version;
              root = builtins.toString ./.;
            })
          ];
        });

      in {
        packages.default = pkg;

        devShells.default = pkgs.mkShell {
          venvDir = "./.venv";
          packages = with python3.pkgs; [
            numba
            pillow
            numpy
            scikit-learn
            venvShellHook
          ];
        };
      });
}
