-- ============================================================================
-- Project        : psyCore
-- Module name    : psyCore_top
-- File type      : VHDL
-- File name      : psyCore_top.vhd
-- Purpose        : top level of the psyCore CPU
-- Author         : QuBi (nitrogenium@outlook.fr)
-- Creation date  : May 30th, 2025
-- ----------------------------------------------------------------------------
-- Best viewed with space indentation (2 spaces)
-- ============================================================================

-- ============================================================================
-- NOTES
-- ============================================================================
-- Description: 
-- TODO

-- Known limitations: 
-- TODO



-- ============================================================================
-- LIBRARIES
-- ============================================================================
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library psycore_lib;
use psycore_lib.psycore_pkg.all;



-- =============================================================================
-- I/Os description
-- =============================================================================
entity psyCore_top is
generic
(
  RESET_POL       : STD_LOGIC;
  RESET_SYNC      : BOOLEAN;
  PIXEL_DATA_BUS  : NATURAL range 1 to 31 := 8;
  H_ACTIVE_POL    : STD_LOGIC := '1';
  V_ACTIVE_POL    : STD_LOGIC := '1'
);
port
( 
  clock           : in STD_LOGIC;
  reset           : in STD_LOGIC; 
  
  someSignal      : out STD_LOGIC_VECTOR(12 downto 0)
);
end psyCore_top;



-- =============================================================================
-- Architecture
-- =============================================================================
architecture archDefault of psyCore_top is
begin

  -- --------------------------------------------------------------------------
  -- VESA core implementation
  -- --------------------------------------------------------------------------
  vesa_core_0 : entity psycore_lib.psycore_core(archDefault)
  generic map
  (
    RESET_POL       => RESET_POL,
    RESET_SYNC      => RESET_SYNC
  )
  port map
  ( 
    clock           => clock,
    reset           => reset,
    
    someOtherSignal => '0'
  );


end archDefault;

