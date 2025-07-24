import React, { useState } from 'react';
import {
  Button,
  Grid,
  Box,
  Typography,
  Tabs,
  Tab,
  Paper,
  Collapse,
} from '@mui/material';
import {
  KeyboardOutlined,
  FunctionsOutlined,
  CalculateOutlined,
  ExpandLess,
  ExpandMore,
} from '@mui/icons-material';

const MathKeyboard = ({ open, onToggle, onSymbolSelect }) => {
  const [activeTab, setActiveTab] = useState(0);

  const symbolCategories = [
    {
      name: 'Basic',
      icon: <KeyboardOutlined />,
      symbols: [
        { symbol: '+', description: 'Plus' },
        { symbol: '−', description: 'Minus' },
        { symbol: '×', description: 'Multiply' },
        { symbol: '÷', description: 'Divide' },
        { symbol: '=', description: 'Equals' },
        { symbol: '≠', description: 'Not equal' },
        { symbol: '<', description: 'Less than' },
        { symbol: '>', description: 'Greater than' },
        { symbol: '≤', description: 'Less than or equal' },
        { symbol: '≥', description: 'Greater than or equal' },
        { symbol: '±', description: 'Plus minus' },
        { symbol: '∓', description: 'Minus plus' },
        { symbol: '(', description: 'Left parenthesis' },
        { symbol: ')', description: 'Right parenthesis' },
        { symbol: '[', description: 'Left bracket' },
        { symbol: ']', description: 'Right bracket' },
        { symbol: '{', description: 'Left brace' },
        { symbol: '}', description: 'Right brace' },
        { symbol: '|', description: 'Absolute value' },
        { symbol: '.', description: 'Decimal point' },
        { symbol: ',', description: 'Comma' },
        { symbol: '%', description: 'Percent' },
        { symbol: ' ', description: 'Space' },
        { symbol: '\t', description: 'Tab' },
      ]
    },
    {
      name: 'Numbers',
      symbols: [
        { symbol: '0', description: 'Zero' },
        { symbol: '1', description: 'One' },
        { symbol: '2', description: 'Two' },
        { symbol: '3', description: 'Three' },
        { symbol: '4', description: 'Four' },
        { symbol: '5', description: 'Five' },
        { symbol: '6', description: 'Six' },
        { symbol: '7', description: 'Seven' },
        { symbol: '8', description: 'Eight' },
        { symbol: '9', description: 'Nine' },
        { symbol: '10', description: 'Ten' },
        { symbol: '100', description: 'Hundred' },
      ]
    },
    {
      name: 'Fractions & Powers',
      icon: <FunctionsOutlined />,
      symbols: [
        { symbol: '½', description: 'One half' },
        { symbol: '⅓', description: 'One third' },
        { symbol: '⅔', description: 'Two thirds' },
        { symbol: '¼', description: 'One quarter' },
        { symbol: '¾', description: 'Three quarters' },
        { symbol: '⅕', description: 'One fifth' },
        { symbol: '⅖', description: 'Two fifths' },
        { symbol: '⅗', description: 'Three fifths' },
        { symbol: '⅘', description: 'Four fifths' },
        { symbol: '⅙', description: 'One sixth' },
        { symbol: '⅚', description: 'Five sixths' },
        { symbol: '⅛', description: 'One eighth' },
        { symbol: '⅜', description: 'Three eighths' },
        { symbol: '⅝', description: 'Five eighths' },
        { symbol: '⅞', description: 'Seven eighths' },
        { symbol: '²', description: 'Squared' },
        { symbol: '³', description: 'Cubed' },
        { symbol: 'ⁿ', description: 'Power n' },
        { symbol: '₁', description: 'Subscript 1' },
        { symbol: '₂', description: 'Subscript 2' },
        { symbol: '₃', description: 'Subscript 3' },
        { symbol: 'ₙ', description: 'Subscript n' },
      ]
    },
    {
      name: 'Roots & Logarithms',
      icon: <CalculateOutlined />,
      symbols: [
        { symbol: '√', description: 'Square root' },
        { symbol: '∛', description: 'Cube root' },
        { symbol: '∜', description: 'Fourth root' },
        { symbol: 'log', description: 'Logarithm' },
        { symbol: 'ln', description: 'Natural log' },
        { symbol: 'lg', description: 'Log base 2' },
        { symbol: 'e', description: 'Euler number' },
        { symbol: 'π', description: 'Pi' },
        { symbol: '∞', description: 'Infinity' },
        { symbol: '∝', description: 'Proportional to' },
        { symbol: '∴', description: 'Therefore' },
        { symbol: '∵', description: 'Because' },
      ]
    },
    {
      name: 'Geometry',
      symbols: [
        { symbol: '°', description: 'Degree' },
        { symbol: '′', description: 'Prime (minutes)' },
        { symbol: '″', description: 'Double prime (seconds)' },
        { symbol: '∠', description: 'Angle' },
        { symbol: '∟', description: 'Right angle' },
        { symbol: '∡', description: 'Measured angle' },
        { symbol: '⊥', description: 'Perpendicular' },
        { symbol: '∥', description: 'Parallel' },
        { symbol: '≅', description: 'Congruent' },
        { symbol: '∼', description: 'Similar' },
        { symbol: '△', description: 'Triangle' },
        { symbol: '□', description: 'Square' },
        { symbol: '○', description: 'Circle' },
      ]
    },
    {
      name: 'Set Theory',
      symbols: [
        { symbol: '∈', description: 'Element of' },
        { symbol: '∉', description: 'Not element of' },
        { symbol: '⊂', description: 'Subset of' },
        { symbol: '⊃', description: 'Superset of' },
        { symbol: '⊆', description: 'Subset of or equal' },
        { symbol: '⊇', description: 'Superset of or equal' },
        { symbol: '∪', description: 'Union' },
        { symbol: '∩', description: 'Intersection' },
        { symbol: '∅', description: 'Empty set' },
        { symbol: 'ℝ', description: 'Real numbers' },
        { symbol: 'ℕ', description: 'Natural numbers' },
        { symbol: 'ℤ', description: 'Integers' },
        { symbol: 'ℚ', description: 'Rational numbers' },
      ]
    },
    {
      name: 'Statistics',
      symbols: [
        { symbol: 'μ', description: 'Mean (mu)' },
        { symbol: 'σ', description: 'Standard deviation' },
        { symbol: 'σ²', description: 'Variance' },
        { symbol: '∑', description: 'Sum' },
        { symbol: '∏', description: 'Product' },
        { symbol: 'x̄', description: 'Sample mean' },
        { symbol: 's', description: 'Sample std dev' },
        { symbol: 'n', description: 'Sample size' },
        { symbol: 'P()', description: 'Probability' },
        { symbol: '!', description: 'Factorial' },
        { symbol: 'C', description: 'Combination' },
        { symbol: 'P', description: 'Permutation' },
      ]
    },
    {
      name: 'Trigonometry',
      symbols: [
        { symbol: 'sin', description: 'Sine' },
        { symbol: 'cos', description: 'Cosine' },
        { symbol: 'tan', description: 'Tangent' },
        { symbol: 'csc', description: 'Cosecant' },
        { symbol: 'sec', description: 'Secant' },
        { symbol: 'cot', description: 'Cotangent' },
        { symbol: 'sin⁻¹', description: 'Arcsine' },
        { symbol: 'cos⁻¹', description: 'Arccosine' },
        { symbol: 'tan⁻¹', description: 'Arctangent' },
        { symbol: 'sinh', description: 'Hyperbolic sine' },
        { symbol: 'cosh', description: 'Hyperbolic cosine' },
        { symbol: 'tanh', description: 'Hyperbolic tangent' },
      ]
    },
    {
      name: 'Calculus',
      symbols: [
        { symbol: '∫', description: 'Integral' },
        { symbol: '∮', description: 'Contour integral' },
        { symbol: '∂', description: 'Partial derivative' },
        { symbol: 'd', description: 'Differential' },
        { symbol: 'Δ', description: 'Delta (change)' },
        { symbol: '∇', description: 'Nabla (gradient)' },
        { symbol: '∆x', description: 'Change in x' },
        { symbol: 'dx', description: 'Differential x' },
        { symbol: 'lim', description: 'Limit' },
        { symbol: '→', description: 'Approaches' },
        { symbol: '∞', description: 'Infinity' },
        { symbol: 'f\'', description: 'Derivative' },
        { symbol: 'f\'\'', description: 'Second derivative' },
      ]
    }
  ];

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleSymbolClick = (symbol) => {
    onSymbolSelect(symbol);
  };

  const currentCategory = symbolCategories[activeTab];

  return (
    <Box sx={{ width: '100%', mt: 2 }}>
      {/* Keyboard Toggle Button */}
      <Button
        variant="outlined"
        onClick={onToggle}
        startIcon={<FunctionsOutlined />}
        endIcon={open ? <ExpandLess /> : <ExpandMore />}
        fullWidth
        sx={{
          justifyContent: 'space-between',
          mb: 1,
          py: 1.5,
          borderStyle: open ? 'solid' : 'dashed',
          borderColor: open ? 'primary.main' : 'grey.400',
          backgroundColor: open ? 'primary.light' : 'transparent',
          color: open ? 'white' : 'text.primary',
          '&:hover': {
            borderStyle: 'solid',
            backgroundColor: 'primary.light',
            color: 'white',
          }
        }}
      >
        {open ? 'Hide Math Keyboard' : 'Show Math Keyboard'}
      </Button>

      {/* Collapsible Math Keyboard */}
      <Collapse in={open} timeout={300}>
        <Paper
          elevation={3}
          sx={{
            border: '1px solid',
            borderColor: 'divider',
            borderRadius: 2,
            overflow: 'hidden'
          }}
        >
          {/* Header */}
          <Box sx={{ px: 2, py: 1, bgcolor: 'grey.50', borderBottom: '1px solid', borderColor: 'divider' }}>
            <Typography variant="h6" component="div" sx={{ fontSize: '1rem', fontWeight: 'bold' }}>
              Math Keyboard
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Click on any symbol to insert it into your answer
            </Typography>
          </Box>

          {/* Tabs */}
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs
              value={activeTab}
              onChange={handleTabChange}
              variant="scrollable"
              scrollButtons="auto"
              sx={{ px: 1 }}
            >
              {symbolCategories.map((category, index) => (
                <Tab
                  key={index}
                  label={category.name}
                  icon={category.icon}
                  iconPosition="start"
                  sx={{ minHeight: 'auto', py: 1, fontSize: '0.875rem' }}
                />
              ))}
            </Tabs>
          </Box>

          {/* Symbol Grid */}
          <Box sx={{ p: 2, maxHeight: '250px', overflowY: 'auto' }}>
            <Grid container spacing={0.5}>
              {currentCategory.symbols.map((item, index) => (
                <Grid item xs={2} sm={1.5} md={1.2} key={index}>
                  <Paper
                    elevation={1}
                    sx={{
                      p: 0.5,
                      textAlign: 'center',
                      cursor: 'pointer',
                      minHeight: '50px',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'center',
                      alignItems: 'center',
                      transition: 'all 0.2s',
                      '&:hover': {
                        elevation: 3,
                        bgcolor: 'primary.light',
                        color: 'white',
                        transform: 'scale(1.05)',
                      },
                      '&:active': {
                        transform: 'scale(0.95)',
                      }
                    }}
                    onClick={() => handleSymbolClick(item.symbol)}
                  >
                    <Typography
                      variant="h6"
                      component="div"
                      sx={{ fontWeight: 'bold', mb: 0.2, fontSize: '1rem' }}
                    >
                      {item.symbol}
                    </Typography>
                    <Typography
                      variant="caption"
                      sx={{
                        fontSize: '0.65rem',
                        textAlign: 'center',
                        lineHeight: 1,
                        opacity: 0.8
                      }}
                    >
                      {item.description}
                    </Typography>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Box>
        </Paper>
      </Collapse>
    </Box>
  );
};

export default MathKeyboard;
