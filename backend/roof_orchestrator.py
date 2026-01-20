import sys
import os

# Ensure backend modules can be imported if running from root
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.agents import (
    GeocodingAgent,
    DataFetchingAgent,
    PreProcessingAgent,
    SegmentationAgent,
    ThreeDReconstructionAgent,
    MeasurementAgent,
    QAAgent,
    ReportingAgent
)

class OrchestratorAgent:
    def __init__(self):
        print("[Orchestrator] Initializing agent workflow...")
        self.geocoder = GeocodingAgent()
        self.data_fetcher = DataFetchingAgent()
        self.preprocessor = PreProcessingAgent()
        self.segmenter = SegmentationAgent()
        self.reconstructor = ThreeDReconstructionAgent()
        self.measurer = MeasurementAgent()
        self.qa = QAAgent()
        self.reporter = ReportingAgent()

    def run(self, request):
        print(f"\n[Orchestrator] Received request: '{request}'")

        # Parse request (simple parsing for now)
        if "Measure roof at" in request:
            address = request.split("Measure roof at")[1].strip()
        else:
            address = "51046 Range Road 224" # Default for testing

        print(f"[Orchestrator] Target Address: {address}")
        print("-" * 50)

        # 1. Geocoding
        location_data = self.geocoder.process(address)

        # 2. Data Fetching
        fetch_result = self.data_fetcher.process(location_data)

        # 3. Pre-processing
        preprocessed_data = self.preprocessor.process(fetch_result)

        # 4. Segmentation
        segmentation_result = self.segmenter.process(preprocessed_data)

        # 5. 3D Reconstruction
        reconstruction_result = self.reconstructor.process(segmentation_result)

        # 6. Measurement
        measurement_result = self.measurer.process(reconstruction_result)

        # 7. QA
        qa_result = self.qa.process(measurement_result)

        if not qa_result['qa_validation']['passed']:
            print("[Orchestrator] QA Failed. Aborting report generation.")
            return None

        # 8. Reporting
        final_output = self.reporter.process(qa_result)

        print("-" * 50)
        print(f"[Orchestrator] Workflow Complete. Report available at: {final_output['report_path']}")
        return final_output

if __name__ == "__main__":
    # Simulate User Request
    user_request = "Measure roof at 51046 Range Road 224"

    orchestrator = OrchestratorAgent()
    result = orchestrator.run(user_request)
