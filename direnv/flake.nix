{
  description = "A Nix-flake-based Python development environment";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" "armv7l-linux" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          venvDir = ".venv";
          packages = with pkgs; [ python312 ] ++
            (with pkgs.python312Packages; [
              pip
              venvShellHook
              numpy
              yfinance
              python-dotenv
              schedule
            ]);
        };
      });
    };
}