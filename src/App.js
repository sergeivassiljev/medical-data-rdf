import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import {
  Form,
  Container,
  Row,
  Col,
  Button,
  Card,
  Spinner,
} from "react-bootstrap";
import { motion } from "framer-motion";
import jsPDF from "jspdf";
import VoiceInput from "./VoiceInput";

function App() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState({
    generated_rdf: "",
    translated_rdf: "",
    medical_report: "",
  });
  const [showTranslated, setShowTranslated] = useState(false);
  const [history, setHistory] = useState([]);
  const [activeHistoryIndex, setActiveHistoryIndex] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showRDFList, setShowRDFList] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/generate_rdf", {
        text,
      });
      setResponse(res.data);
      setHistory((prevHistory) => [
        ...prevHistory,
        { text, response: res.data },
      ]);
    } catch (error) {
      console.error("Error while sending:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    setIsLoading(true);
    try {
      const res = await axios.post(
        "http://localhost:5000/generate_medical_report",
        {
          rdf_data: response.generated_rdf,
        }
      );
      setResponse((prevState) => ({
        ...prevState,
        medical_report: res.data.generated_report,
      }));
    } catch (error) {
      console.error("Error while sending:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const downloadPDF = () => {
    const doc = new jsPDF();

    doc.setFont("helvetica", "normal");

    const margins = { top: 20, left: 20, right: 20 };
    const pageHeight = doc.internal.pageSize.height;

    doc.setFontSize(18);
    doc.text("Medical Report", margins.left, 30);

    doc.setFontSize(12);
    doc.text("Date: " + new Date().toLocaleDateString(), margins.left, 40);

    let currentHeight = 50;

    const textLines = doc.splitTextToSize(
      response.medical_report,
      doc.internal.pageSize.width - margins.left - margins.right
    );

    textLines.forEach((line) => {
      if (currentHeight + 10 > pageHeight - 20) {
        doc.addPage();
        currentHeight = margins.top;
      }
      doc.text(line, margins.left, currentHeight);
      currentHeight += 10;
    });

    doc.save("medical_report.pdf");
  };

  const renderRDFParts = (rdfString) => {
    const lines = rdfString.split("\n");
    const parts = [];
    let currentPart = [];
    let currentPartTitle = "";

    lines.forEach((line) => {
      if (line.startsWith("Part")) {
        if (currentPart.length > 0) {
          parts.push({ title: currentPartTitle, triples: [...currentPart] });
          currentPart = [];
        }
        currentPartTitle = line.trim();
      } else if (line.startsWith("-")) {
        currentPart.push(line.substring(1).trim());
      }
    });

    if (currentPart.length > 0) {
      parts.push({ title: currentPartTitle, triples: [...currentPart] });
    }

    return parts.map((part, index) => (
      <div key={index}>
        <h5>{part.title}</h5>
        <ul>
          {part.triples.map((triple, tripleIndex) => (
            <li key={tripleIndex}>{triple}</li>
          ))}
        </ul>
      </div>
    ));
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col lg={8}>
          <Card className="mb-4 shadow-sm">
            <Card.Body>
              <h2 className="mb-4">
                Generate and translate RDF from medical text
              </h2>
              <Form onSubmit={handleSubmit}>
                <Form.Group>
                  <Form.Label>Enter medical data:</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows="4"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                  />
                </Form.Group>
                <VoiceInput />
                <Button variant="primary" type="submit" className="mt-2">
                  Generate RDF
                </Button>
              </Form>
              {isLoading && (
                <div className="d-flex justify-content-center my-2">
                  <Spinner animation="border" role="status">
                    <span className="sr-only">Loading...</span>
                  </Spinner>
                </div>
              )}
            </Card.Body>
          </Card>
          <Form>
            <Form.Check
              type="switch"
              id="custom-switch"
              label={showTranslated ? "Translated RDF" : "Generated RDF"}
              checked={showTranslated}
              onChange={() => setShowTranslated(!showTranslated)}
              className="mb-3"
            />
          </Form>
          <Card className="shadow-sm mb-3">
            <Card.Body>
              <Card.Title>
                {showTranslated ? "Translated RDF:" : "Generated RDF:"}
              </Card.Title>
              <Card.Text>
                {showTranslated
                  ? response.translated_rdf
                  : response.generated_rdf}
              </Card.Text>
            </Card.Body>
          </Card>
          <Button
            variant="secondary"
            onClick={() => setShowRDFList(!showRDFList)}
            className="mb-3"
          >
            Get list
          </Button>
          {showRDFList &&
            renderRDFParts(
              showTranslated ? response.translated_rdf : response.generated_rdf
            )}
        </Col>
        <Col lg={4}>
          <div className="history-panel">
            <h5>History of requests</h5>
            {history.map((item, index) => (
              <motion.div
                key={index}
                initial={{ x: 50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ duration: 0.5 }}
                className={`history-item mb-2 p-2 bg-light border rounded ${
                  index === activeHistoryIndex ? "bg-info text-white" : ""
                }`}
                onClick={() => {
                  setResponse(item.response);
                  setActiveHistoryIndex(index);
                }}
              >
                {item.text.substring(0, 50)}...
              </motion.div>
            ))}
          </div>
        </Col>
      </Row>
      <Button variant="success" onClick={handleGenerateReport} className="mt-2">
        Generate Medical Report
      </Button>
      {response.medical_report && (
        <>
          <Card className="shadow-sm mb-3">
            <Card.Body>
              <Card.Title>Generated Medical Report:</Card.Title>
              <Card.Text style={{ whiteSpace: "pre-wrap" }}>
                {response.medical_report}
              </Card.Text>
            </Card.Body>
          </Card>
          <Button variant="success" onClick={downloadPDF} className="mb-3">
            Download as PDF
          </Button>
        </>
      )}
    </Container>
  );
}

export default App;
