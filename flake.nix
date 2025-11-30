{
  description = "atk-fw-util nix shell";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-parts.url = "github:hercules-ci/flake-parts";

  outputs = { flake-parts, ... } @ inputs: flake-parts.lib.mkFlake { inherit inputs; } {
    perSystem = {pkgs, ...}: {
      devShells.default =
        pkgs.mkShell {
          packages = with pkgs; [
            python3
            python3Packages.pyusb
            poetry
          ];
        };
    };
    systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
  };
}
