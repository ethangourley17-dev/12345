"""
Job Manager Module
Manages roofing job tracking and status
"""

import json
from datetime import datetime


class JobManager:
    """Manages roofing jobs and their status"""
    
    def __init__(self):
        self.jobs = []
    
    def create_job(self, address, customer_name, roof_area_sqft, estimated_cost):
        """
        Create a new roofing job
        
        Args:
            address (str): Property address
            customer_name (str): Customer name
            roof_area_sqft (float): Roof area in square feet
            estimated_cost (float): Estimated project cost
        
        Returns:
            dict: Created job details
        """
        job = {
            "job_id": len(self.jobs) + 1,
            "address": address,
            "customer_name": customer_name,
            "roof_area_sqft": roof_area_sqft,
            "estimated_cost": estimated_cost,
            "status": "Pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.jobs.append(job)
        return job
    
    def get_job(self, job_id):
        """
        Get job details by ID
        
        Args:
            job_id (int): Job ID
        
        Returns:
            dict: Job details or None if not found
        """
        for job in self.jobs:
            if job["job_id"] == job_id:
                return job
        return None
    
    def update_job_status(self, job_id, status):
        """
        Update job status
        
        Args:
            job_id (int): Job ID
            status (str): New status (e.g., "Pending", "In Progress", "Completed")
        
        Returns:
            bool: True if updated, False if job not found
        """
        for job in self.jobs:
            if job["job_id"] == job_id:
                job["status"] = status
                job["updated_at"] = datetime.now().isoformat()
                return True
        return False
    
    def list_jobs(self, status_filter=None):
        """
        List all jobs, optionally filtered by status
        
        Args:
            status_filter (str): Optional status to filter by
        
        Returns:
            list: List of jobs
        """
        if status_filter:
            return [job for job in self.jobs if job["status"] == status_filter]
        return self.jobs
    
    def delete_job(self, job_id):
        """
        Delete a job by ID
        
        Args:
            job_id (int): Job ID
        
        Returns:
            bool: True if deleted, False if job not found
        """
        for i, job in enumerate(self.jobs):
            if job["job_id"] == job_id:
                self.jobs.pop(i)
                return True
        return False
    
    def export_jobs_json(self):
        """
        Export all jobs as JSON string
        
        Returns:
            str: JSON representation of all jobs
        """
        return json.dumps(self.jobs, indent=2)
    
    def import_jobs_json(self, json_str):
        """
        Import jobs from JSON string
        
        Args:
            json_str (str): JSON string containing jobs data
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.jobs = json.loads(json_str)
            return True
        except Exception as e:
            print(f"Error importing jobs: {e}")
            return False
