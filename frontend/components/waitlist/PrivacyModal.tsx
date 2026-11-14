"use client";

import React from "react";
import { Modal } from "@/components/ui/Modal";

interface PrivacyModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function PrivacyModal({ isOpen, onClose }: PrivacyModalProps) {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Privacy & Abuse Protection">
      <div className="text-xs text-neutral-300 space-y-2.5 leading-relaxed">
        <p>
          <strong>What we collect:</strong> Your name, email address, and the product concept reserved.
        </p>
        <p>
          <strong>Data Storage:</strong> Records are saved securely in hosted PostgreSQL (Supabase) with Row Level Security (RLS) enabled.
        </p>
        <p>
          <strong>Abuse Protection:</strong> Honeypot traps and per-IP rate limits block bots.
        </p>
        <p>
          <strong>Right to Deletion:</strong> You can permanently delete your data at any time via the privacy deletion endpoint.
        </p>
      </div>
      <div className="pt-4 text-right">
        <button
          onClick={onClose}
          type="button"
          className="px-4 py-2 rounded-xl bg-emerald-500 text-black font-semibold text-xs hover:bg-emerald-400 cursor-pointer"
        >
          Understood
        </button>
      </div>
    </Modal>
  );
}
