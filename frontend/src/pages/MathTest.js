import React from 'react';
import { Container, Typography, Box, Card, CardContent, Button } from '@mui/material';
import { MathText } from '../components/MathRenderer';
import { useNavigate } from 'react-router-dom';

const MathTest = () => {
  const navigate = useNavigate();

  const testExamples = [
    {
      title: "Product-to-Sum Identity",
      text: "Verify the Product-to-Sum Identity:\n\\[\n\\sin A \\cos B = \\frac{1}{2} [\\sin(A + B) + \\sin(A - B)]\n\\]\nby expressing \\(\\sin A \\cos B\\) as a sum of sines using known identities"
    },
    {
      title: "Trigonometric Function",
      text: "Find the angle \\(\\theta\\) where \\(0° ≤ \\theta ≤ 360°\\) if \\(\\sin \\theta = \\frac{\\sqrt{3}}{2}\\)"
    },
    {
      title: "Quadratic Formula",
      text: "Solve using the quadratic formula: \\(x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\) for \\(ax^2 + bx + c = 0\\)"
    },
    {
      title: "Integration",
      text: "Evaluate the integral \\(\\int_0^{\\pi/2} \\sin(x) \\, dx\\)"
    },
    {
      title: "Complex Numbers",
      text: "Find the modulus of the complex number \\(z = 3 + 4i\\) using \\(|z| = \\sqrt{a^2 + b^2}\\)"
    }
  ];

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Math Rendering Test
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
          This page demonstrates LaTeX math rendering in Mathopedia questions.
        </Typography>
        <Button variant="outlined" onClick={() => navigate('/grade-selection')}>
          Back to Grade Selection
        </Button>
      </Box>

      {testExamples.map((example, index) => (
        <Card key={index} sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom color="primary">
              {example.title}
            </Typography>
            <Box className="math-question">
              <MathText>{example.text}</MathText>
            </Box>
          </CardContent>
        </Card>
      ))}

      <Box sx={{ mt: 4, p: 3, bgcolor: 'grey.50', borderRadius: 2 }}>
        <Typography variant="h6" gutterBottom>
          Math Rendering Features:
        </Typography>
        <Typography variant="body2" component="div">
          • <strong>Inline Math:</strong> Use \\( \\) for inline expressions like \\(x^2 + y^2 = z^2\\)<br/>
          • <strong>Block Math:</strong> Use \\[ \\] for centered equations<br/>
          • <strong>Symbols:</strong> Greek letters (\\(\\alpha, \\beta, \\theta\\)), fractions, integrals<br/>
          • <strong>Functions:</strong> Trigonometric, logarithmic, and other mathematical functions<br/>
          • <strong>Responsive:</strong> Scales properly on all devices
        </Typography>
      </Box>
    </Container>
  );
};

export default MathTest;
