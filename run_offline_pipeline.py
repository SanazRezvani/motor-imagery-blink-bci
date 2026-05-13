import os
import numpy as np

from src.config import (
    CSV_PATH,
    RESULTS_DIR,
    SFREQ,
    EEG_CHANNELS,
    EOG_CHANNELS,
    DECODING_CHANNELS,
    EVENT_ID,
    TMIN,
    TMAX,
    BANDPASS_LOW,
    BANDPASS_HIGH,
    RANDOM_STATE,
    CSP_COMPONENTS,
)

from src.load_data import load_csv
from src.mne_processing import (
    create_raw_from_dataframe,
    filter_raw,
    create_events_from_cues,
    create_epochs,
)

from src.feature_extraction import (
    extract_epoch_features,
    label_epochs_with_blinks,
    extract_csp_features,
)


from src.classification import train_evaluate_classifier

from src.visualisation import (
    plot_eeg_heo_blinks_with_cues_dual_axis,
    plot_clean_vs_blink_accuracy,
)


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print("Loading multimodal EEG CSV...")
    df = load_csv(CSV_PATH)

    print(f"Loaded data shape: {df.shape}")


    print("Creating MNE Raw object...")
    raw = create_raw_from_dataframe(
        df=df,
        eeg_channels=EEG_CHANNELS,
        eog_channels=EOG_CHANNELS,
        sfreq=SFREQ,
    )

    print(raw)

    print("Filtering EEG in mu/beta range...")
    raw_filtered = filter_raw(
        raw,
        low_freq=BANDPASS_LOW,
        high_freq=BANDPASS_HIGH,
    )

    print("Creating events from Cues column...")
    events = create_events_from_cues(df, EVENT_ID)

    print(f"Number of events found: {len(events)}")

    print("Creating epochs...")
    epochs = create_epochs(
        raw_filtered,
        events,
        EVENT_ID,
        tmin=TMIN,
        tmax=TMAX,
    )

    print(epochs)

    # Keep good channels
    epochs = epochs.copy().pick(DECODING_CHANNELS)
    print(f"Using channels: {DECODING_CHANNELS}")

    # Extracting CSP features
    print("Extracting CSP features...")

    X, y, csp = extract_csp_features(
        epochs,
        decoding_channels=DECODING_CHANNELS,
        n_components=CSP_COMPONENTS,
    )

    print(f"CSP feature matrix shape: {X.shape}")

    y = epochs.events[:, -1]

    print(f"Feature matrix shape: {X.shape}")

    print("Labelling epochs as clean or blink-contaminated...")
    blink_labels = label_epochs_with_blinks(
        df=df,
        events=events,
        tmin=TMIN,
        tmax=TMAX,
        sfreq=SFREQ,
    )

    clean_mask = blink_labels == 0

    print(f"Clean epochs: {clean_mask.sum()}")
    print(f"Blink-contaminated epochs: {(~clean_mask).sum()}")

    print("\nTraining classifier on all epochs...")
    model_all, acc_all, report_all = train_evaluate_classifier(
        X,
        y,
        random_state=RANDOM_STATE,
    )

    print(f"Accuracy using all epochs: {acc_all:.3f}")
    print(report_all)

    print("\nTraining classifier on clean epochs only...")

    if clean_mask.sum() > 5 and len(np.unique(y[clean_mask])) == 2:
        model_clean, acc_clean, report_clean = train_evaluate_classifier(
            X[clean_mask],
            y[clean_mask],
            random_state=RANDOM_STATE,
        )

        print(f"Accuracy using clean epochs only: {acc_clean:.3f}")
        print(report_clean)

    else:
        acc_clean = np.nan
        print("Not enough clean epochs from both classes for clean-only classification.")

    print("Creating figures...")

    plot_eeg_heo_blinks_with_cues_dual_axis(
        df=df,
        results_dir=RESULTS_DIR,
        start_time=20,
        end_time=40,
        eeg_channel="C3",
        heo_channel="HEO",
    )

    if not np.isnan(acc_clean):
        plot_clean_vs_blink_accuracy(
            clean_accuracy=acc_clean,
            all_accuracy=acc_all,
            results_dir=RESULTS_DIR,
        )

    print("\nPipeline complete.")
    print(f"Results saved to: {RESULTS_DIR}")


if __name__ == "__main__":
    main()